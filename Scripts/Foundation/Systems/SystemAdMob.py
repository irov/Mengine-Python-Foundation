from Foundation.System import System
from Foundation.Utils import SimpleLogger
from Foundation.Providers.AdvertisementProvider import AdvertisementProvider
from Foundation.Systems.Ads.AdFactory import AdFactory

_Log = SimpleLogger("SystemAdMob")

ANDROID_PLUGIN_NAME = "MengineAdMob"
APPLE_PLUGIN_NAME = "AppleAdMob"

DEVDEBUGGER_TAB_NAME = "AdMob"

class SystemAdMob(System):
    """ Advertisement module 'AdMob' """

    is_plugin_active = False
    is_sdk_init = False

    def __init__(self):
        super(SystemAdMob, self).__init__()
        self.banner = AdFactory.createAd("Banner")
        self.interstitial = AdFactory.createAd("Interstitial")
        self.rewarded = AdFactory.createAd("Rewarded")
        self.semaphoreAdServiceReady = Semaphore(False, "AdServiceReady")

    @staticmethod
    def _onAvailable(params):
        if _ANDROID:
            SystemAdMob.is_plugin_active = Mengine.isAvailablePlugin(ANDROID_PLUGIN_NAME)
        elif _IOS:
            SystemAdMob.is_plugin_active = Mengine.isAvailablePlugin(APPLE_PLUGIN_NAME)
            pass

        return SystemAdMob.is_plugin_active
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
            IsShowingInterstitialAdvert=self.isShowingInterstitial,
            # rewarded:
            HasRewardedAdvert=self.hasRewarded,
            CanOfferRewardedAdvert=self.canOfferRewarded,
            CanYouShowRewardedAdvert=self.canYouShowRewarded,
            ShowRewardedAdvert=self.showRewarded,
            IsShowingRewardedAdvert=self.isShowingRewarded,
            # consent flow:
            ShowConsentFlow=self.showConsentFlow,
            IsConsentFlow=self.isConsentFlow,
        )

        AdvertisementProvider.setProvider("AdMob", methods)

    @staticmethod
    def isSdkInitialized():
        return SystemAdMob.is_sdk_init is True

    def getBannerHeight(self):
        if _IOS:
            return Mengine.appleAdvertisementGetBannerWidth()
        elif _ANDROID:
            return Mengine.androidIntegerMethod(ANDROID_PLUGIN_NAME, "getBannerHeight")
        return None

    def getBannerWidth(self):
        if _IOS:
            return Mengine.appleAdvertisementGetBannerHeight()
        elif _ANDROID:
            return Mengine.androidIntegerMethod(ANDROID_PLUGIN_NAME, "getBannerWidth")
        return None

    # callbacks

    def __cbSdkInitialized(self):
        _Log("[SDK cb] onAdMobPluginOnSdkInitialized")
        SystemAdMob.is_sdk_init = True
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

    def isShowingInterstitial(self):
        return self.interstitial.isShowing()

    def hasRewarded(self):
        return self.rewarded.has()

    def canOfferRewarded(self, placement):
        return self.rewarded.canOffer(placement)

    def canYouShowRewarded(self, placement):
        return self.rewarded.canYouShow(placement)

    def showRewarded(self, placement):
        return self.rewarded.show(placement)

    def isShowingRewarded(self):
        return self.rewarded.isShowing()

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
