from Foundation.Providers.AdvertisementProvider import AdvertisementProvider
from Foundation.System import System
from Foundation.Utils import SimpleLogger
from Notification import Notification

_Log = SimpleLogger("SystemApplovin")
PLUGIN_NAME = "AppLovin"

class SystemApplovin(System):
    """ Advertisement module 'Applovin' """

    class AdUnitMixin(object):
        ad_type = None
        s_callbacks = {"onAdDisplayed": None, "onAdDisplayFailed": None, "onAdClicked": None, "onAdHidden": None, }
        s_androidmethods = {"init": None, "show": None, "can_offer": None, "is_available": None, }

        def __init__(self):
            self.inited = False
            self.ad_unit_id = Menge.getConfigString(PLUGIN_NAME + "Plugin", "%sAdUnitId" % self.ad_type, "")

        def setCallbacks(self):
            if _ANDROID:
                Menge.setAndroidCallback(PLUGIN_NAME, self.s_callbacks["onAdDisplayed"], self.cbDisplaySuccess)
                Menge.setAndroidCallback(PLUGIN_NAME, self.s_callbacks["onAdDisplayFailed"], self.cbDisplayFailed)
                Menge.setAndroidCallback(PLUGIN_NAME, self.s_callbacks["onAdClicked"], self.cbClicked)
                Menge.setAndroidCallback(PLUGIN_NAME, self.s_callbacks["onAdHidden"], self.cbHidden)

        def init(self):
            if bool(Menge.getConfigBool('Advertising', self.ad_type, False)) is False:
                return False
            if self.ad_unit_id == "":
                _Log("[{}] call init failed: ad unit id is not configured or wrong ({})!".format(self.ad_type, self.ad_unit_id), err=True)
                return False

            _Log("[{}] call init".format(self.ad_type))
            Menge.androidMethod(PLUGIN_NAME, self.s_androidmethods["init"], self.ad_unit_id)

            self.inited = True

            return True

        def canOffer(self):
            """ Call this method only once when you create rewarded button """
            if self.s_androidmethods["can_offer"] is None:
                return True
            status = Menge.androidBooleanMethod(PLUGIN_NAME, self.s_androidmethods["can_offer"])
            _Log("[{}] available to offer is {}".format(self.ad_type, status))
            return status

        def isAvailable(self):
            """ Call this method if you 100% will show ad, but want to do something before show """
            status = Menge.androidBooleanMethod(PLUGIN_NAME, self.s_androidmethods["is_available"])
            _Log("[{}] available to show is {}".format(self.ad_type, status))
            return status

        def show(self):
            if self.__checkInit() is False:
                return False

            _Log("[{}] show advertisement...".format(self.ad_type))
            if Menge.androidBooleanMethod(PLUGIN_NAME, self.s_androidmethods["show"]) is False:
                self.cbDisplayFailed()
            return True

        # utils

        def __checkInit(self, init_if_no=False):
            """ returns True if ad inited else False
                @param init_if_no: if True - tries to init """

            if self.ad_unit_id is None:
                return False

            if self.inited is True:
                return True
            err_msg = "Applovin ad [{}] not inited".format(self.ad_type)

            if init_if_no is True:
                err_msg += ". Try init..."
                self.init()

            _Log(err_msg, err=True)
            return False

        def getProviderMethods(self):
            return {"Show{}Advert".format(self.ad_type): self.show, "CanOffer{}Advert".format(self.ad_type): self.canOffer, "Is{}AdvertAvailable".format(self.ad_type): self.isAvailable}

        # callbacks

        def cbDisplaySuccess(self):
            Notification.notify(Notificator.onAdvertDisplayed, self.ad_type)
            _Log("[{} cb] displayed".format(self.ad_type))

        def cbDisplayFailed(self):
            Notification.notify(Notificator.onAdvertDisplayFailed, self.ad_type)
            _Log("[{} cb] !!! display failed".format(self.ad_type))

        def cbHidden(self):
            Notification.notify(Notificator.onAdvertHidden, self.ad_type)
            _Log("[{} cb] hidden".format(self.ad_type))

        def cbClicked(self):
            Notification.notify(Notificator.onAdvertClicked, self.ad_type)
            _Log("[{} cb] clicked".format(self.ad_type))

        # devtodebug

        def _getDevToDebugWidgets(self):
            widgets = []

            # descr widget

            is_enable = bool(Menge.getConfigBool('Advertising', self.ad_type, False))

            def _getDescr():
                text = "### {}".format(self.ad_type)
                text += "\nenable in configs.json: `{}`".format(is_enable)
                text += "\ninited: `{}`".format(self.inited)
                return text

            w_descr = Menge.createDevToDebugWidgetText(self.ad_type + "_descr")
            w_descr.setText(_getDescr)
            widgets.append(w_descr)

            # button widgets

            methods = {"init": self.init, "show": self.show, }
            for key, method in methods.items():
                w_btn = Menge.createDevToDebugWidgetButton(self.ad_type + "_" + key)
                w_btn.setTitle(key)
                w_btn.setClickEvent(method)
                widgets.append(w_btn)

            return widgets

    class InterstitialAd(AdUnitMixin):
        ad_type = "Interstitial"
        s_callbacks = {"onAdDisplayed": "onApplovinInterstitialOnAdDisplayed", "onAdDisplayFailed": "onApplovinInterstitialOnAdDisplayFailed", "onAdClicked": "onApplovinInterstitialOnAdClicked", "onAdHidden": "onApplovinInterstitialOnAdHidden", }
        s_androidmethods = {"init": "initInterstitial", "show": "showInterstitial", "is_available": "canYouShowInterstitial", }

    class RewardedAd(AdUnitMixin):
        ad_type = "Rewarded"
        s_callbacks = {"onAdDisplayed": "onApplovinRewardedOnAdDisplayed", "onAdDisplayFailed": "onApplovinRewardedOnAdDisplayFailed", "onAdClicked": "onApplovinRewardedOnAdClicked", "onAdHidden": "onApplovinRewardedOnAdHidden", "onVideoStarted": "onApplovinRewardedOnRewardedVideoStarted", "onVideoCompleted": "onApplovinRewardedOnRewardedVideoCompleted", "onUserRewarded": "onApplovinRewardedOnUserRewarded", }
        s_androidmethods = {"init": "initRewarded", "show": "showRewarded", "can_offer": "canOfferRewarded", "is_available": "canYouShowRewarded", }

        def setCallbacks(self):
            super(self.__class__, self).setCallbacks()
            if _ANDROID:
                Menge.setAndroidCallback(PLUGIN_NAME, self.s_callbacks["onVideoStarted"], self.cbVideoStarted)
                Menge.setAndroidCallback(PLUGIN_NAME, self.s_callbacks["onVideoCompleted"], self.cbVideoCompleted)
                Menge.setAndroidCallback(PLUGIN_NAME, self.s_callbacks["onUserRewarded"], self.cbUserRewarded)

        def cbVideoStarted(self):
            _Log("[{} cb] video started".format(self.ad_type))

        def cbVideoCompleted(self):
            _Log("[{} cb] video completed".format(self.ad_type))
            Notification.notify(Notificator.onAdvertCompleted, self.ad_type)

        def cbUserRewarded(self, label, reward):
            Notification.notify(Notificator.onAdvertRewarded, label, reward)
            _Log("[{} cb] user rewarded: {}={!r}".format(self.ad_type, label, reward))

    # ---

    b_plugin = _PLUGINS.get(PLUGIN_NAME, False)
    b_sdk_init = False

    def __init__(self):
        super(SystemApplovin, self).__init__()
        self.interstitial = None
        self.rewarded = None

    def _onInitialize(self):
        if self.b_plugin is False:
            return

        self.interstitial = SystemApplovin.InterstitialAd()
        self.rewarded = SystemApplovin.RewardedAd()

        if _ANDROID:
            # cb on init Applovin sdk
            Menge.waitAndroidSemaphore("AppLovinSdkInitialized", self.__cbSdkInitialized)

        # Interstitial advertisements (player is obligated to watch these ads)
        self.interstitial.setCallbacks()

        # Rewarded advertisements (the player can watch ads at will and get reward after full view)
        self.rewarded.setCallbacks()

        # ads do init in `__cbSdkInitialized`
        self.__addDevToDebug()

    # utils

    def initAds(self):
        self.rewarded.init()
        self.interstitial.init()

        provider_methods = dict()
        provider_methods.update(self.rewarded.getProviderMethods())
        provider_methods.update(self.interstitial.getProviderMethods())
        AdvertisementProvider.setProvider(PLUGIN_NAME, provider_methods)

    @staticmethod
    def isSdkInitialized():
        return SystemApplovin.b_sdk_init is True

    @staticmethod
    def showMediationDebugger():
        Menge.androidMethod(PLUGIN_NAME, "showMediationDebugger")

    # callbacks

    def __cbSdkInitialized(self):
        _Log("[SDK cb] onApplovinPluginOnSdkInitialized")
        SystemApplovin.b_sdk_init = True
        self.initAds()

        self.__disableDevToDebugInitButton()

    # devtodebug

    def __disableDevToDebugInitButton(self):
        if Menge.isAvailablePlugin("DevToDebug") is False:
            return
        if Menge.hasDevToDebugTab(PLUGIN_NAME) is False:
            return

        tab = Menge.getDevToDebugTab(PLUGIN_NAME)
        widget = tab.findWidget("run_init")
        if widget:
            widget.setHide(True)

    def __addDevToDebug(self):
        if Menge.isAvailablePlugin("DevToDebug") is False:
            return
        if self.b_plugin is False:
            return
        if Menge.hasDevToDebugTab(PLUGIN_NAME) is True:
            return

        tab = Menge.addDevToDebugTab(PLUGIN_NAME)
        widgets = []

        if self.b_sdk_init is False:
            w_init = Menge.createDevToDebugWidgetButton("run_init")
            w_init.setTitle("Run init applovin")
            w_init.setClickEvent(Menge.androidMethod, PLUGIN_NAME, "initialize")
            widgets.append(w_init)

        w_debug = Menge.createDevToDebugWidgetButton("show_mediation_debugger")
        w_debug.setTitle("Show Mediation Debugger")
        w_debug.setClickEvent(self.showMediationDebugger)
        widgets.append(w_debug)

        widgets.extend(self.rewarded._getDevToDebugWidgets())
        widgets.extend(self.interstitial._getDevToDebugWidgets())

        for widget in widgets:
            tab.addWidget(widget)

    def __remDevToDebug(self):
        if Menge.isAvailablePlugin("DevToDebug") is False:
            return
        if Menge.hasDevToDebugTab(PLUGIN_NAME) is False:
            return

        Menge.removeDevToDebugTab(PLUGIN_NAME)