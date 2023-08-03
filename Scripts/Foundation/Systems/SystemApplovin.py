from Foundation.Providers.AdvertisementProvider import AdvertisementProvider
from Foundation.System import System
from Foundation.Utils import SimpleLogger
from Notification import Notification

_Log = SimpleLogger("SystemApplovin")
PLUGIN_NAME = "AppLovin"
# todo: add banners


def ad_callback(bound_method):
    def wrap(self, ad_unit_id, *args, **kwargs):
        if ad_unit_id != self.ad_unit_id:
            return
        return bound_method(self, *args, **kwargs)
    return wrap


class SystemApplovin(System):
    """ Advertisement module 'Applovin' """

    class AdUnitMixin(object):
        ad_type = None
        s_callbacks = {
            "onAdDisplayed": None,
            "onAdDisplayFailed": None,
            "onAdClicked": None,
            "onAdHidden": None,
        }
        s_androidmethods = {
            "init": None,
            "show": None,
            "can_offer": None,
            "is_available": None,
        }

        def __init__(self, name):
            self.inited = False
            self.display = False
            self.name = name
            self.ad_unit_id = Mengine.getConfigString(PLUGIN_NAME + "Plugin", "%sAdUnitId" % self.name, "")

        def setCallbacks(self):
            if _ANDROID:
                Mengine.setAndroidCallback(PLUGIN_NAME, self.s_callbacks["onAdDisplayed"], self.cbDisplaySuccess)
                Mengine.setAndroidCallback(PLUGIN_NAME, self.s_callbacks["onAdDisplayFailed"], self.cbDisplayFailed)
                Mengine.setAndroidCallback(PLUGIN_NAME, self.s_callbacks["onAdClicked"], self.cbClicked)
                Mengine.setAndroidCallback(PLUGIN_NAME, self.s_callbacks["onAdHidden"], self.cbHidden)

        def init(self):
            if bool(Mengine.getConfigBool('Advertising', self.ad_type, False)) is False:
                return False
            if self.ad_unit_id == "":
                _Log("[{}] call init failed: ad unit id is not configured or wrong ({})!".format(self.name, self.ad_unit_id), err=True)
                return False

            _Log("[{}] call init".format(self.name))
            Mengine.androidMethod(PLUGIN_NAME, self.s_androidmethods["init"], self.ad_unit_id)

            self.inited = True

            return True

        def cleanUp(self):
            if _ANDROID:
                Mengine.removeAndroidCallback(PLUGIN_NAME, self.s_callbacks["onAdDisplayed"], self.cbDisplaySuccess)
                Mengine.removeAndroidCallback(PLUGIN_NAME, self.s_callbacks["onAdDisplayFailed"], self.cbDisplayFailed)
                Mengine.removeAndroidCallback(PLUGIN_NAME, self.s_callbacks["onAdClicked"], self.cbClicked)
                Mengine.removeAndroidCallback(PLUGIN_NAME, self.s_callbacks["onAdHidden"], self.cbHidden)

        def canOffer(self):
            """ Call this method only once when you create rewarded button """
            if self.s_androidmethods["can_offer"] is None:
                return True
            status = Mengine.androidBooleanMethod(PLUGIN_NAME, self.s_androidmethods["can_offer"], self.ad_unit_id)
            _Log("[{}] available to offer is {}".format(self.name, status))
            return status

        def isAvailable(self):
            """ Call this method if you 100% will show ad, but want to do something before show """
            status = Mengine.androidBooleanMethod(PLUGIN_NAME, self.s_androidmethods["is_available"], self.ad_unit_id)
            _Log("[{}] available to show is {}".format(self.name, status))
            return status

        def show(self):
            if self.__checkInit() is False:
                self.cbDisplayFailed(self.ad_unit_id)
                return False

            _Log("[{}] show advertisement...".format(self.name))
            if Mengine.androidBooleanMethod(PLUGIN_NAME, self.s_androidmethods["show"], self.ad_unit_id) is False:
                self.cbDisplayFailed(self.ad_unit_id)
            return True

        # utils

        def __checkInit(self, init_if_no=False):
            """ returns True if ad inited else False
                @param init_if_no: if True - tries to init """

            if self.ad_unit_id is None:
                return False

            if self.inited is True:
                return True
            err_msg = "Applovin ad [{}] not inited".format(self.name)

            if init_if_no is True:
                err_msg += ". Try init..."
                self.init()

            _Log(err_msg, err=True)
            return False

        # callbacks

        @ad_callback
        def cbDisplaySuccess(self):
            self.display = True
            Notification.notify(Notificator.onAdvertDisplayed, self.ad_type, self.name)
            _Log("[{} cb] displayed".format(self.name))

        @ad_callback
        def cbDisplayFailed(self):
            Notification.notify(Notificator.onAdvertDisplayFailed, self.ad_type, self.name)
            _Log("[{} cb] !!! display failed".format(self.name), err=True, force=True)

        @ad_callback
        def cbHidden(self):
            self.display = False
            Notification.notify(Notificator.onAdvertHidden, self.ad_type, self.name)
            _Log("[{} cb] hidden".format(self.name))

        @ad_callback
        def cbClicked(self):
            Notification.notify(Notificator.onAdvertClicked, self.ad_type, self.name)
            _Log("[{} cb] clicked".format(self.name))

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

            methods = {"init": self.init, "show": self.show, }
            for key, method in methods.items():
                w_btn = Mengine.createDevToDebugWidgetButton(self.name + "_" + key)
                w_btn.setTitle(key)
                w_btn.setClickEvent(method)
                widgets.append(w_btn)

            return widgets

    class InterstitialAd(AdUnitMixin):
        """ player is obligated to watch these ads """

        ad_type = "Interstitial"
        s_callbacks = {
            "onAdDisplayed": "onApplovinInterstitialOnAdDisplayed",
            "onAdDisplayFailed": "onApplovinInterstitialOnAdDisplayFailed",
            "onAdClicked": "onApplovinInterstitialOnAdClicked",
            "onAdHidden": "onApplovinInterstitialOnAdHidden",
        }
        s_androidmethods = {
            "init": "initInterstitial",
            "show": "showInterstitial",
            "is_available": "canYouShowInterstitial",
        }

    class RewardedAd(AdUnitMixin):
        """ player could watch ad without skip and get reward after full view """

        ad_type = "Rewarded"
        s_callbacks = {
            "onAdDisplayed": "onApplovinRewardedOnAdDisplayed",
            "onAdDisplayFailed": "onApplovinRewardedOnAdDisplayFailed",
            "onAdClicked": "onApplovinRewardedOnAdClicked",
            "onAdHidden": "onApplovinRewardedOnAdHidden",
            "onUserRewarded": "onApplovinRewardedOnUserRewarded",
        }
        s_androidmethods = {
            "init": "initRewarded",
            "show": "showRewarded",
            "can_offer": "canOfferRewarded",
            "is_available": "canYouShowRewarded",
        }

        def __init__(self, name):
            super(self.__class__, self).__init__(name)
            self.rewarded = False

        def setCallbacks(self):
            super(self.__class__, self).setCallbacks()
            if _ANDROID:
                Mengine.addAndroidCallback(PLUGIN_NAME, self.s_callbacks["onUserRewarded"], self.cbUserRewarded)

        def cleanUp(self):
            super(self.__class__, self).cleanUp()
            if _ANDROID:
                Mengine.removeAndroidCallback(self.s_callbacks["onUserRewarded"], self.cbUserRewarded)

        @ad_callback
        def cbUserRewarded(self, label, reward):
            self.rewarded = True
            Notification.notify(Notificator.onAdvertRewarded, self.name, label, reward)
            _Log("[{} cb] user rewarded: label={!r}, amount={!r}".format(self.name, label, reward))

        @ad_callback
        def cbDisplaySuccess(self):
            self.rewarded = False
            super(self.__class__, self).cbDisplaySuccess(self.ad_unit_id)

        @ad_callback
        def cbHidden(self):
            if self.rewarded is False:
                Notification.notify(Notificator.onAdvertSkipped, self.ad_type, self.name)
                _Log("[{} cb] advert {!r} was skipped".format(self.ad_type, self.name))
            super(self.__class__, self).cbHidden(self.ad_unit_id)

    # ---

    b_plugin = _PLUGINS.get(PLUGIN_NAME, False)
    b_sdk_init = False

    def __init__(self):
        super(SystemApplovin, self).__init__()
        self.interstitials = {}
        self.rewardeds = {}

    def _onInitialize(self):
        if self.b_plugin is False:
            return

        init_params = [
            ["RewardedUnitNames", ["Rewarded"], self.rewardeds, SystemApplovin.RewardedAd],
            ["InterstitialUnitNames", ["Interstitial"], self.interstitials, SystemApplovin.InterstitialAd],
        ]

        for config_key, default_values, storage, Type in init_params:
            unit_names = Mengine.getConfigStrings("Advertising", config_key)
            if len(unit_names) == 0:
                unit_names = default_values

            for name in unit_names:
                if name in storage:
                    _Log("Duplicate name {} in {}".format(name, Type.ad_type), err=True)
                    continue

                rewarded = Type(name)
                storage[name] = rewarded

        if _ANDROID:
            # cb on init Applovin sdk
            Mengine.waitAndroidSemaphore("AppLovinSdkInitialized", self.__cbSdkInitialized)

        for ad_unit in self._getAllAdUnits():
            ad_unit.setCallbacks()

        # ads do init in `__cbSdkInitialized`
        self.__addDevToDebug()

    def _onFinalize(self):
        for ad_unit in self._getAllAdUnits():
            ad_unit.cleanUp()
        self.rewardeds = None
        self.interstitials = None

    # utils

    def initAds(self):
        for ad_unit in self._getAllAdUnits():
            ad_unit.init()

        provider_methods = dict(
            ShowRewardedAdvert=Functor(self.showAdvert, self.rewardeds),
            ShowInterstitialAdvert=Functor(self.showAdvert, self.interstitials),
            CanOfferRewardedAdvert=Functor(self.canOfferAdvert, self.rewardeds),
            IsRewardedAdvertAvailable=Functor(self.isAdvertAvailable, self.rewardeds),
            IsInterstitialAdvertAvailable=Functor(self.isAdvertAvailable, self.interstitials),
        )
        AdvertisementProvider.setProvider(PLUGIN_NAME, provider_methods)

    @staticmethod
    def isSdkInitialized():
        return SystemApplovin.b_sdk_init is True

    @staticmethod
    def showMediationDebugger():
        Mengine.androidMethod(PLUGIN_NAME, "showMediationDebugger")

    def _getAllAdUnits(self):
        return self.rewardeds.values() + self.interstitials.values()

    # callbacks

    def __cbSdkInitialized(self):
        _Log("[SDK cb] onApplovinPluginOnSdkInitialized")
        SystemApplovin.b_sdk_init = True
        self.initAds()

        self.__disableDevToDebugInitButton()

    # provider handling

    def showAdvert(self, ad_unit_name, advert_dict):
        advert = advert_dict.get(ad_unit_name)
        if advert is None:
            Trace.log("System", 0, "Advert {!r} not found for showAdvert in {}".format(
                ad_unit_name, advert_dict.keys()))
            return False
        return advert.show()

    def canOfferAdvert(self, ad_unit_name, advert_dict):
        advert = advert_dict.get(ad_unit_name)
        if advert is None:
            Trace.log("System", 0, "Advert {!r} not found for canOfferAdvert in {}".format(
                ad_unit_name, advert_dict.keys()))
            return False
        return advert.canOffer()

    def isAdvertAvailable(self, ad_unit_name, advert_dict):
        advert = advert_dict.get(ad_unit_name)
        if advert is None:
            Trace.log("System", 0, "Advert {!r} not found for isAdvertAvailable in {}".format(
                ad_unit_name, advert_dict.keys()))
            return False
        return advert.isAvailable()

    # debug

    def __disableDevToDebugInitButton(self):
        if Mengine.isAvailablePlugin("DevToDebug") is False:
            return
        if Mengine.hasDevToDebugTab(PLUGIN_NAME) is False:
            return

        tab = Mengine.getDevToDebugTab(PLUGIN_NAME)
        widget = tab.findWidget("run_init")
        if widget:
            widget.setHide(True)

    def __addDevToDebug(self):
        if Mengine.isAvailablePlugin("DevToDebug") is False:
            return
        if self.b_plugin is False:
            return
        if Mengine.hasDevToDebugTab(PLUGIN_NAME) is True:
            return

        tab = Mengine.addDevToDebugTab(PLUGIN_NAME)
        widgets = []

        if self.b_sdk_init is False:
            w_init = Mengine.createDevToDebugWidgetButton("run_init")
            w_init.setTitle("Run init applovin")
            w_init.setClickEvent(Mengine.androidMethod, PLUGIN_NAME, "initialize")
            widgets.append(w_init)

        w_debug = Mengine.createDevToDebugWidgetButton("show_mediation_debugger")
        w_debug.setTitle("Show Mediation Debugger")
        w_debug.setClickEvent(self.showMediationDebugger)
        widgets.append(w_debug)

        for ad_unit in self._getAllAdUnits():
            widgets.extend(ad_unit._getDevToDebugWidgets())

        for widget in widgets:
            tab.addWidget(widget)

    def __remDevToDebug(self):
        if Mengine.isAvailablePlugin("DevToDebug") is False:
            return
        if Mengine.hasDevToDebugTab(PLUGIN_NAME) is False:
            return

        Mengine.removeDevToDebugTab(PLUGIN_NAME)
