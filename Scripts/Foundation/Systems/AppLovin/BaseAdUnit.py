from Foundation.Utils import SimpleLogger


_Log = SimpleLogger("SystemApplovin")
CREDENTIALS_CONFIG_KEY = "AppLovinPlugin"


def ad_callback(bound_method):
    if _ANDROID:
        # I add callback, that returns an `ad_unit_id` as first argument
        def cb_wrapper(self, *args, **kwargs):
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

    def __init__(self):
        super(BaseAdUnit, self).__init__()
        self.inited = False

    def initialize(self):
        if bool(Mengine.getConfigBool('Advertising', self.ad_type, False)) is False:
            return False

        self._log("[{}] call init".format(self.ad_type))

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

    def has(self, placement):
        if self.__checkInit() is False:
            return False

        return self._has(placement)

    def _has(self, placement):
        raise NotImplementedError

    def canOffer(self, placement):
        """ Call this method only once when you create rewarded button """

        status = self._canOffer(placement)
        self._log("[{}] available to offer {} is {}".format(self.ad_type, placement, status))

        return status

    def _canOffer(self, placement):
        raise NotImplementedError

    def canYouShow(self, placement):
        """ Call this method if you 100% will show ad, but want to do something before show """

        status = self._canYouShow(placement)
        self._log("[{}] available to show {} is {}".format(self.ad_type, placement, status))

        return status

    def _canYouShow(self, placement):
        raise NotImplementedError

    def show(self, placement):
        if self.__checkInit() is False:
            self._cbShowCompleted(False, {"placement": placement})
            return False

        self._log("[{}] show {}".format(self.ad_type, placement))

        if self._show(placement) is False:
            self._cbShowCompleted(False, {"placement": placement})
            return False

        return True

    def _show(self, placement):
        raise NotImplementedError

    def hide(self, placement):
        if self.__checkInit() is False:
            self._cbShowCompleted(False, {"placement": placement})
            return False

        self._log("[{}] hide {}".format(self.ad_type, placement))

        if self._hide(placement) is False:
            self._cbShowCompleted(False, {"placement": placement})
            return False

        return True

    def _hide(self, placement):
        raise NotImplementedError

    # utils

    def __checkInit(self, init_if_no=False):
        """ returns True if ad inited else False
            @param init_if_no: if True - tries to init """
        if self.inited is True:
            return True
        err_msg = "Applovin ad [{}] not inited".format(self.ad_type)

        if init_if_no is True:
            err_msg += ". Try init..."
            status = self.initialize()
            err_msg += " Status {}".format(status)

        self._log(err_msg, err=True, force=True)
        return False

    def _log(self, *args, **kwargs):
        _Log(*args, **kwargs)

    # callbacks

    @ad_callback
    def cbShowCompleted(self, successful, params):
        self._cbShowCompleted(successful, params)

    def _cbShowCompleted(self, successful, params):
        self._log("[{} cb] completed {}".format(self.ad_type, params))
        Notification.notify(Notificator.onAdShowCompleted, self.ad_type, successful, params)

    @ad_callback
    def cbRevenuePaid(self, params):
        self._cbRevenuePaid(params)

    def _cbRevenuePaid(self, params):
        self._log("[{} cb] pay revenue {}".format(self.ad_type, params))
        Notification.notify(Notificator.onAdRevenuePaid, self.ad_type, params)

    # devtodebug

    def _getDevToDebugWidgets(self):
        widgets = []

        # descr widget

        is_enable = bool(Mengine.getConfigBool('Advertising', self.ad_type, False))

        def __getDescr():
            text = "### [{}]".format(self.ad_type)
            text += "\nenable in configs.json: `{}`".format(is_enable)
            text += "\ninited: `{}`".format(self.inited)
            return text

        w_descr = Mengine.createDevToDebugWidgetText(self.ad_type + "_descr")
        w_descr.setText(__getDescr)
        widgets.append(w_descr)

        # button widgets

        methods = {"init": self.initialize, "show": self.show, }
        for key, method in methods.items():
            w_btn = Mengine.createDevToDebugWidgetButton(self.ad_type + "_" + key)
            w_btn.setTitle(key)
            w_btn.setClickEvent(method)
            widgets.append(w_btn)

        return widgets


class AndroidAdUnitCallbacks(object):
    ANDROID_PLUGIN_NAME = "MengineAdService"

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
