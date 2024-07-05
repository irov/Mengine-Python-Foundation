from Foundation.System import System
from Foundation.Utils import SimpleLogger
from Foundation.Providers.AdvertisementProvider import AdvertisementProvider
from Foundation.Systems.AppLovin.AppLovinAdFactory import AppLovinAdFactory


_Log = SimpleLogger("SystemApplovin")

ANDROID_PLUGIN_NAME = "MengineAppLovin"
APPLE_PLUGIN_NAME = "AppleAppLovin"

DEVDEBUGGER_TAB_NAME = "Applovin"


class SystemApplovin(System):
    """ Advertisement module 'Applovin' """

    is_plugin_active = False
    is_sdk_init = False

    def __init__(self):
        super(SystemApplovin, self).__init__()
        self.interstitials = {}
        self.rewardeds = {}
        self.banners = {}

    def _onInitialize(self):
        if _ANDROID:
            SystemApplovin.is_plugin_active = Mengine.isAvailablePlugin(ANDROID_PLUGIN_NAME)
        elif _IOS:
            SystemApplovin.is_plugin_active = Mengine.isAvailablePlugin(APPLE_PLUGIN_NAME)

        if self.is_plugin_active is False:
            return

        init_params = [
            ["RewardedUnitNames", ["Rewarded"], self.rewardeds, "Rewarded"],
            ["InterstitialUnitNames", ["Interstitial"], self.interstitials, "Interstitial"],
            ["BannerUnitNames", ["Banner"], self.banners, "Banner"],
        ]

        for config_key, default_values, storage, ad_type in init_params:
            if Mengine.getConfigBool("Advertising", ad_type, False) is False:
                # this ad type is not active - enable in Configs.json
                continue

            unit_names = Mengine.getConfigStrings("Advertising", config_key)
            if len(unit_names) == 0:
                unit_names = default_values

            for name in unit_names:
                if name in storage:
                    _Log("Duplicate name {} in {}".format(name, ad_type), err=True)
                    continue

                ad_unit = AppLovinAdFactory.createAd(ad_type, name)
                storage[name] = ad_unit

        Mengine.waitSemaphore("AppLovinSdkInitialized", self.__cbSdkInitialized)

        # ads do init in `__cbSdkInitialized`
        self.__addDevToDebug()

    def _onFinalize(self):
        for ad_unit in self._getAllAdUnits():
            ad_unit.cleanUp()
        self.rewardeds = None
        self.interstitials = None
        self.banners = None

    # utils

    def initAds(self):
        for ad_unit in self._getAllAdUnits():
            if ad_unit.initialize() is False:
                Trace.log("System", 0, "Failed to init advert [{}:{}]".format(ad_unit.ad_type, ad_unit.name))

        provider_methods = dict(
            ShowRewardedAdvert=Functor(self.showAdvert, self.rewardeds),
            ShowInterstitialAdvert=Functor(self.showAdvert, self.interstitials),
            CanOfferRewardedAdvert=Functor(self.canOfferAdvert, self.rewardeds),
            IsRewardedAdvertAvailable=Functor(self.isAdvertAvailable, self.rewardeds),
            IsInterstitialAdvertAvailable=Functor(self.isAdvertAvailable, self.interstitials),
            ShowBanner=Functor(self.showAdvert, self.banners),
            HideBanner=Functor(self.hideBanner, self.banners),
            ShowConsentFlow=self.showConsentFlow,
            IsConsentFlow=self.isConsentFlow,
            GetBannerViewport=self.getBannerViewport,
        )
        AdvertisementProvider.setProvider(ANDROID_PLUGIN_NAME, provider_methods)

    @staticmethod
    def isSdkInitialized():
        return SystemApplovin.is_sdk_init is True

    @staticmethod
    def showMediationDebugger():
        if _ANDROID:
            Mengine.androidMethod(ANDROID_PLUGIN_NAME, "showMediationDebugger")
        elif _IOS:
            Mengine.appleAppLovinShowMediationDebugger()

    def showConsentFlow(self):
        if _ANDROID:
            Mengine.androidMethod(ANDROID_PLUGIN_NAME, "showConsentFlow")
        elif _IOS:
            Mengine.appleAppLovinLoadAndShowCMPFlow({
                "onAppleAppLovinConsentFlowShowSuccessful": self.__cbConsentFlowShowSuccessful,
                "onAppleAppLovinConsentFlowShowFailed": self.__cbConsentFlowShowFailed,
            })

    def isConsentFlow(self):
        if _ANDROID:
            return Mengine.androidBooleanMethod(ANDROID_PLUGIN_NAME, "isConsentFlowUserGeographyGDPR")
        elif _IOS:
            return Mengine.appleAppLovinIsConsentFlowUserGeographyGDPR()
        return False

    def getBannerViewport(self):
        if _IOS:
            return Mengine.appleAppLovinGetBannerViewport()
        elif _ANDROID:
            return Mengine.androidMethod(ANDROID_PLUGIN_NAME, "getBannerViewport")
        return None

    def _getAllAdUnits(self):
        return self.rewardeds.values() + self.interstitials.values() + self.banners.values()

    # callbacks

    def __cbSdkInitialized(self):
        _Log("[SDK cb] onAppLovinPluginOnSdkInitialized")
        SystemApplovin.is_sdk_init = True
        self.initAds()

        self.__disableDevToDebugInitButton()

    def __cbConsentFlowShowSuccessful(self):
        _Log("[cb] Consent Flow Show Successful")

    def __cbConsentFlowShowFailed(self):
        _Log("[cb] Consent Flow Show Failed", err=True, force=True)

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

    def hideBanner(self, ad_unit_name, banners_dict):
        banner = banners_dict.get(ad_unit_name)
        if banner is None:
            Trace.log("System", 0, "Banner {!r} not found for hideBanner in {}".format(
                ad_unit_name, banners_dict.keys()))
            return False
        return banner.hide()

    # debug

    def __disableDevToDebugInitButton(self):
        if Mengine.isAvailablePlugin("DevToDebug") is False:
            return
        if Mengine.hasDevToDebugTab(DEVDEBUGGER_TAB_NAME) is False:
            return

        tab = Mengine.getDevToDebugTab(DEVDEBUGGER_TAB_NAME)
        widget = tab.findWidget("run_init")
        if widget:
            widget.setHide(True)

    def __addDevToDebug(self):
        if Mengine.isAvailablePlugin("DevToDebug") is False:
            return
        if self.is_plugin_active is False:
            return
        if Mengine.hasDevToDebugTab(DEVDEBUGGER_TAB_NAME) is True:
            return

        tab = Mengine.addDevToDebugTab(DEVDEBUGGER_TAB_NAME)
        widgets = []

        if self.is_sdk_init is False and _ANDROID:
            w_init = Mengine.createDevToDebugWidgetButton("run_init")
            w_init.setTitle("Run init applovin")
            w_init.setClickEvent(Mengine.androidMethod, ANDROID_PLUGIN_NAME, "initialize")
            widgets.append(w_init)

        w_debug = Mengine.createDevToDebugWidgetButton("show_mediation_debugger")
        w_debug.setTitle("Show Mediation Debugger")
        w_debug.setClickEvent(self.showMediationDebugger)
        widgets.append(w_debug)

        w_consent = Mengine.createDevToDebugWidgetButton("show_consent_flow")
        w_consent.setTitle("Show Consent Flow (isConsentFlow={})".format(self.isConsentFlow()))
        w_consent.setClickEvent(self.showConsentFlow)
        widgets.append(w_consent)

        for ad_unit in self._getAllAdUnits():
            widgets.extend(ad_unit._getDevToDebugWidgets())

        for widget in widgets:
            tab.addWidget(widget)

    def __remDevToDebug(self):
        if Mengine.isAvailablePlugin("DevToDebug") is False:
            return
        if Mengine.hasDevToDebugTab(DEVDEBUGGER_TAB_NAME) is False:
            return

        Mengine.removeDevToDebugTab(DEVDEBUGGER_TAB_NAME)
