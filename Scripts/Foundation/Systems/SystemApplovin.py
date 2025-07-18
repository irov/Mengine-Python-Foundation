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
        self.banner = AppLovinAdFactory.createAd("Banner")
        self.interstitial = AppLovinAdFactory.createAd("Interstitial")
        self.rewarded = AppLovinAdFactory.createAd("Rewarded")
        self.semaphoreAdServiceReady = Semaphore(False, "AdServiceReady")

    @staticmethod
    def _onAvailable(params):
        if _ANDROID:
            SystemApplovin.is_plugin_active = Mengine.isAvailablePlugin(ANDROID_PLUGIN_NAME)
        elif _IOS:
            SystemApplovin.is_plugin_active = Mengine.isAvailablePlugin(APPLE_PLUGIN_NAME)
            pass

        return SystemApplovin.is_plugin_active
        pass

    def _onInitialize(self):
        Mengine.waitSemaphore("AdServiceReady", self.__cbSdkInitialized)

        # ads do init in `__cbSdkInitialized`
        self.__addDevToDebug()

    def _onFinalize(self):
        if self.banner is not None:
            self.banner.cleanUp()
            self.banner = None

        if self.interstitial is not None:
            self.interstitial.cleanUp()
            self.interstitial = None

        if self.rewarded is not None:
            self.rewarded.cleanUp()
            self.rewarded = None

    def _onPreparation(self, source):
        source.addSemaphore(self.semaphoreAdServiceReady, From=True)

    def initAds(self):
        if Mengine.getConfigBool("Advertising", self.banner.ad_type, False) is True:
            if self.banner.initialize() is False:
                Trace.log("System", 0, "Failed to init banner advert")
                pass
            pass

        if Mengine.getConfigBool("Advertising", self.interstitial.ad_type, False) is True:
            if self.interstitial.initialize() is False:
                Trace.log("System", 0, "Failed to init interstitial advert")
                pass
            pass

        if Mengine.getConfigBool("Advertising", self.rewarded.ad_type, False) is True:
            if self.rewarded.initialize() is False:
                Trace.log("System", 0, "Failed to init rewarded advert")
                pass
            pass

        methods = dict(
            # banner:
            ShowBanner=self.showBanner,
            HideBanner=self.hideBanner,
            GetBannerHeight=self.getBannerHeight,
            GetBannerWidth=self.getBannerWidth,
            # interstitial:
            HasInterstitialAdvert=self.hasInterstitial,
            CanYouShowInterstitialAdvert=self.canYouShowInterstitial,
            ShowInterstitialAdvert=self.showInterstitial,
            # rewarded:
            HasRewardedAdvert=self.hasRewarded,
            CanOfferRewardedAdvert=self.canOfferRewarded,
            CanYouShowRewardedAdvert=self.canYouShowRewarded,
            ShowRewardedAdvert=self.showRewarded,
            # consent flow:
            ShowConsentFlow=self.showConsentFlow,
            IsConsentFlow=self.isConsentFlow,
        )

        AdvertisementProvider.setProvider("AppLovin", methods)

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
            def __cbConsentFlowShowSuccess(self):
                _Log("[cb] Consent Flow Show Successful")

            def __cbConsentFlowShowFailed(self):
                _Log("[cb] Consent Flow Show Failed", err=True, force=True)

            Mengine.appleAppLovinLoadAndShowCMPFlow(dict(
                onAppleAppLovinConsentFlowShowSuccess=__cbConsentFlowShowSuccess,
                onAppleAppLovinConsentFlowShowFailed=__cbConsentFlowShowFailed,
            ))

    def isConsentFlow(self):
        if _ANDROID:
            return Mengine.androidBooleanMethod(ANDROID_PLUGIN_NAME, "isConsentFlowUserGeographyGDPR")
        elif _IOS:
            return Mengine.appleAppLovinIsConsentFlowUserGeographyGDPR()
        return False

    def getBannerHeight(self):
        if _IOS:
            return Mengine.appleAppLovinGetBannerHeight()
        elif _ANDROID:
            return Mengine.androidIntegerMethod(ANDROID_PLUGIN_NAME, "getBannerHeight")
        return None

    def getBannerWidth(self):
        if _IOS:
            return Mengine.appleAppLovinGetBannerWidth()
        elif _ANDROID:
            return Mengine.androidIntegerMethod(ANDROID_PLUGIN_NAME, "getBannerWidth")
        return None

    # callbacks

    def __cbSdkInitialized(self):
        _Log("[SDK cb] onAppLovinPluginOnSdkInitialized")
        SystemApplovin.is_sdk_init = True
        self.initAds()

        self.__disableDevToDebugInitButton()
        self.semaphoreAdServiceReady.setValue(True)

    # provider handling

    def showBanner(self):
        return self.banner.show("banner")

    def hideBanner(self):
        return self.banner.hide("banner")

    def hasInterstitial(self):
        return self.interstitial.has()

    def canYouShowInterstitial(self, placement):
        return self.interstitial.canYouShow(placement)

    def showInterstitial(self, placement):
        return self.interstitial.show(placement)

    def hasRewarded(self):
        return self.rewarded.has()

    def canOfferRewarded(self, placement):
        return self.rewarded.canOffer(placement)

    def canYouShowRewarded(self, placement):
        return self.rewarded.canYouShow(placement)

    def showRewarded(self, placement):
        return self.rewarded.show(placement)

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

        w_debug = Mengine.createDevToDebugWidgetButton("show_mediation_debugger")
        w_debug.setTitle("Show Mediation Debugger")
        w_debug.setClickEvent(self.showMediationDebugger)
        widgets.append(w_debug)

        w_consent = Mengine.createDevToDebugWidgetButton("show_consent_flow")
        w_consent.setTitle("Show Consent Flow (isConsentFlow={})".format(self.isConsentFlow()))
        w_consent.setClickEvent(self.showConsentFlow)
        widgets.append(w_consent)

        widgets.extend(self.banner._getDevToDebugWidgets())
        widgets.extend(self.interstitial._getDevToDebugWidgets())
        widgets.extend(self.rewarded._getDevToDebugWidgets())

        for widget in widgets:
            tab.addWidget(widget)

    def __remDevToDebug(self):
        if Mengine.isAvailablePlugin("DevToDebug") is False:
            return
        if Mengine.hasDevToDebugTab(DEVDEBUGGER_TAB_NAME) is False:
            return

        Mengine.removeDevToDebugTab(DEVDEBUGGER_TAB_NAME)
