from Foundation.Utils import SimpleLogger


_Log = SimpleLogger("SystemApplovin")
CREDENTIALS_CONFIG_KEY = "AppLovinPlugin"


def ad_callback(bound_method):
    if _ANDROID:
        # I add callback, that returns an `ad_unit_id` as first argument
        def cb_wrapper(self, ad_unit_id, *args, **kwargs):
            if ad_unit_id != self.ad_unit_id:
                return
            return bound_method(self, *args, **kwargs)
    elif _IOS:
        # each callback is bounded to a specific ad unit
        def cb_wrapper(self, *args, **kwargs):
            return bound_method(self, *args, **kwargs)
    else:
        def cb_wrapper(self, *args, **kwargs):
            return bound_method(self, *args, **kwargs)
    return cb_wrapper


class BaseAdUnit(object):
    ad_type = None

    def __init__(self, name):
        super(BaseAdUnit, self).__init__()
        self.inited = False
        self.display = False
        self.name = name    # placement
        self.ad_unit_id = Mengine.getConfigString(CREDENTIALS_CONFIG_KEY, "%sAdUnitId" % self.name, "")

    def initialize(self):
        if bool(Mengine.getConfigBool('Advertising', self.ad_type, False)) is False:
            return False
        if self.ad_unit_id == "":
            self._log("[{}] call init failed: ad unit id is not configured or wrong ({})!".format(self.name, self.ad_unit_id), err=True, force=True)
            return False

        self._log("[{}] call init".format(self.name))

        if self._initialize() is True:
            self.inited = True
            return True

        return False

    def _initialize(self):
        raise NotImplementedError

    def cleanUp(self):
        self._cleanUp()

    def _cleanUp(self):
        return

    def canOffer(self):
        """ Call this method only once when you create rewarded button """

        status = self._canOffer()
        self._log("[{}:{}] available to offer is {}".format(self.ad_type, self.name, status))

        return status

    def _canOffer(self):
        raise NotImplementedError

    def isAvailable(self):
        """ Call this method if you 100% will show ad, but want to do something before show """

        status = self._isAvailable()
        self._log("[{}:{}] available to show is {}".format(self.ad_type, self.name, status))

        return status

    def _isAvailable(self):
        raise NotImplementedError

    def show(self):
        if self.__checkInit() is False:
            self._cbDisplayFailed()
            return False

        self._log("[{}:{}] show advertisement...".format(self.ad_type, self.name))

        if self._show() is False:
            self._cbDisplayFailed()
            return False

        return True

    def _show(self):
        raise NotImplementedError

    # utils

    def __checkInit(self, init_if_no=False):
        """ returns True if ad inited else False
            @param init_if_no: if True - tries to init """

        if self.ad_unit_id is None:
            return False

        if self.inited is True:
            return True
        err_msg = "Applovin ad [{}:{}:{}] not inited".format(self.ad_type, self.name, self.ad_unit_id)

        if init_if_no is True:
            err_msg += ". Try init..."
            status = self.initialize()
            err_msg += " Status {}".format(status)

        self._log(err_msg, err=True, force=True)
        return False

    def getPlacementName(self):
        return self.name

    def _log(self, *args, **kwargs):
        _Log(*args, **kwargs)

    # callbacks

    @ad_callback
    def cbDisplaySuccess(self):
        self._cbDisplaySuccess()

    def _cbDisplaySuccess(self):
        self.display = True
        self._log("[{} cb] displayed".format(self.name))
        Notification.notify(Notificator.onAdvertDisplayed, self.ad_type, self.name)

    @ad_callback
    def cbDisplayFailed(self):
        self._cbDisplayFailed()

    def _cbDisplayFailed(self):
        self._log("[{} cb] !!! display failed".format(self.name), err=True, force=True)
        Notification.notify(Notificator.onAdvertDisplayFailed, self.ad_type, self.name)

    @ad_callback
    def cbHidden(self):
        self._cbHidden()

    def _cbHidden(self):
        self.display = False
        self._log("[{} cb] hidden".format(self.name))
        Notification.notify(Notificator.onAdvertHidden, self.ad_type, self.name)

    @ad_callback
    def cbClicked(self):
        self._cbClicked()

    def _cbClicked(self):
        self._log("[{} cb] clicked".format(self.name))
        Notification.notify(Notificator.onAdvertClicked, self.ad_type, self.name)

    @ad_callback
    def cbLoadSuccess(self):
        self._cbLoadSuccess()

    def _cbLoadSuccess(self):
        self._log("[{} cb] load success".format(self.name))
        Notification.notify(Notificator.onAdvertLoadSuccess, self.ad_type, self.name)

    @ad_callback
    def cbLoadFailed(self):
        self._cbLoadFailed()

    def _cbLoadFailed(self):
        self._log("[{} cb] !!! load failed".format(self.name), err=False, force=True)
        Notification.notify(Notificator.onAdvertLoadFail, self.ad_type, self.name)

    @ad_callback
    def cbPayRevenue(self, revenue_data=None):
        """ revenue_data = {'revenue': float} """
        if revenue_data is None:    # fixme
            revenue_data = {}
        self._cbPayRevenue(revenue_data)

    def _cbPayRevenue(self, revenue_data):
        self._log("[{} cb] pay revenue {}".format(self.name, revenue_data))
        revenue = revenue_data.get('revenue', 0.0)
        Notification.notify(Notificator.onAdvertPayRevenue, self.ad_type, self.name, revenue)

    # devtodebug

    def _getDevToDebugWidgets(self):
        widgets = []

        # descr widget

        is_enable = bool(Mengine.getConfigBool('Advertising', self.ad_type, False))

        def _getDescr():
            text = "### [{}] {}".format(self.ad_type, self.name)
            text += "\nenable in configs.json: `{}`".format(is_enable)
            text += "\ninited: `{}`".format(self.inited)
            return text

        w_descr = Mengine.createDevToDebugWidgetText(self.name + "_descr")
        w_descr.setText(_getDescr)
        widgets.append(w_descr)

        # button widgets

        methods = {"init": self.initialize, "show": self.show, }
        for key, method in methods.items():
            w_btn = Mengine.createDevToDebugWidgetButton(self.name + "_" + key)
            w_btn.setTitle(key)
            w_btn.setClickEvent(method)
            widgets.append(w_btn)

        return widgets


class AndroidAdUnitCallbacks(object):
    ANDROID_PLUGIN_NAME = "MengineAppLovin"

    def __init__(self):
        super(AndroidAdUnitCallbacks, self).__init__()
        self._cbs = {}

    def _addAndroidCallback(self, name, cb):
        if name in self._cbs:
            Trace.log("System", 0, "{}: callback {!r} is already exists !!!".format(self.__class__.__name__, name))
            Mengine.removeAndroidCallback(self.ANDROID_PLUGIN_NAME, name, self._cbs[name])
        identity = Mengine.addAndroidCallback(self.ANDROID_PLUGIN_NAME, name, cb)
        self._cbs[name] = identity
        return identity

    def _setCallbacks(self):
        raise NotImplementedError

    def _removeAndroidCallbacks(self):
        for name, cb_id in self._cbs.items():
            Mengine.removeAndroidCallback(self.ANDROID_PLUGIN_NAME, name, cb_id)
        self._cbs = {}
