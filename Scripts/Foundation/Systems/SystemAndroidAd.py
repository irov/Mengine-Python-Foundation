from Foundation.Providers.AdvertisementProvider import AdvertisementProvider
from Foundation.Task.Semaphore import Semaphore
from Foundation.Systems.SystemAndroid import SystemAndroid
from Foundation.Utils import SimpleLogger

_Log = SimpleLogger("SystemAdService")

ANDROID_ADSERVICE_PLUGIN_NAME = "AndroidAdServicePlugin"


class SystemAndroidAd(SystemAndroid):
    def __init__(self):
        super(SystemAndroidAd, self).__init__()

        self.semaphoreAdServiceReady = Semaphore(False, "AdServiceReady")
        self.banner_inited = False
        self.interstitial_inited = False
        self.rewarded_inited = False

    def _onFinalize(self):
        self._removeAndroidCallbacks(ANDROID_ADSERVICE_PLUGIN_NAME)
        self.banner_inited = False
        self.interstitial_inited = False
        self.rewarded_inited = False

    def _onPreparation(self, source):
        source.addSemaphore(self.semaphoreAdServiceReady, From=True)

    def _setAdServiceReady(self, value=True):
        self.semaphoreAdServiceReady.setValue(value)

    def initAds(self):
        if Mengine.getConfigBool("Advertising", "Banner", False) is True:
            if self._initializeBannerAd() is False:
                Trace.log("System", 0, "Failed to init banner advert")

        if Mengine.getConfigBool("Advertising", "Interstitial", False) is True:
            if self._initializeInterstitialAd() is False:
                Trace.log("System", 0, "Failed to init interstitial advert")

        if Mengine.getConfigBool("Advertising", "Rewarded", False) is True:
            if self._initializeRewardedAd() is False:
                Trace.log("System", 0, "Failed to init rewarded advert")

        return dict(
            ShowBanner=self.showBanner,
            HideBanner=self.hideBanner,
            GetBannerHeight=self.getBannerHeight,
            GetBannerWidth=self.getBannerWidth,
            HasInterstitialAdvert=self.hasInterstitialAdvert,
            CanYouShowInterstitialAdvert=self.canYouShowInterstitialAdvert,
            ShowInterstitialAdvert=self.showInterstitialAdvert,
            IsShowingInterstitialAdvert=self.isShowingInterstitialAdvert,
            HasRewardedAdvert=self.hasRewardedAdvert,
            CanOfferRewardedAdvert=self.canOfferRewardedAdvert,
            CanYouShowRewardedAdvert=self.canYouShowRewardedAdvert,
            ShowRewardedAdvert=self.showRewardedAdvert,
            IsShowingRewardedAdvert=self.isShowingRewardedAdvert,
            GetNoAds=self.getNoAds,
        )

    def getBannerWidth(self):
        return self._androidIntegerMethod(ANDROID_ADSERVICE_PLUGIN_NAME, "getBannerWidth")

    def getBannerHeight(self):
        return self._androidIntegerMethod(ANDROID_ADSERVICE_PLUGIN_NAME, "getBannerHeight")

    def getNoAds(self):
        return self._androidBooleanMethod(ANDROID_ADSERVICE_PLUGIN_NAME, "getNoAds")

    def showBanner(self):
        if self.banner_inited is False:
            self.__logAd("ad showBanner not inited", trace=True, err=True, force=True)
            return False

        self.__logAd("[Banner] show banner")
        return self._androidMethod(ANDROID_ADSERVICE_PLUGIN_NAME, "showBanner")

    def hideBanner(self):
        if self.banner_inited is False:
            self.__logAd("ad hideBanner not inited", trace=True, err=True, force=True)
            return False

        self.__logAd("[Banner] hide banner")
        return self._androidMethod(ANDROID_ADSERVICE_PLUGIN_NAME, "hideBanner")

    def hasInterstitialAdvert(self):
        return self._androidBooleanMethod(ANDROID_ADSERVICE_PLUGIN_NAME, "hasInterstitial")

    def canYouShowInterstitialAdvert(self, placement):
        if self.interstitial_inited is False:
            self.__logAd("ad canYouShowInterstitial not inited", trace=True, err=True, force=True)
            return False

        status = self._androidBooleanMethod(ANDROID_ADSERVICE_PLUGIN_NAME, "canYouShowInterstitial", placement)
        self.__logAd("[Interstitial] available to show {} is {}".format(placement, status))
        return status

    def showInterstitialAdvert(self, placement):
        if self.interstitial_inited is False:
            self.__logAd("ad showInterstitial not inited", trace=True, err=True, force=True)
            return False

        self.__logAd("[Interstitial] show {}".format(placement))
        return self._androidBooleanMethod(ANDROID_ADSERVICE_PLUGIN_NAME, "showInterstitial", placement)

    def isShowingInterstitialAdvert(self):
        if self.interstitial_inited is False:
            self.__logAd("ad isShowingInterstitial not inited", trace=True, err=True, force=True)
            return False

        return self._androidBooleanMethod(ANDROID_ADSERVICE_PLUGIN_NAME, "isShowingInterstitial")

    def hasRewardedAdvert(self):
        return self._androidBooleanMethod(ANDROID_ADSERVICE_PLUGIN_NAME, "hasRewarded")

    def canOfferRewardedAdvert(self, placement):
        if self.rewarded_inited is False:
            self.__logAd("ad canOfferRewarded not inited", trace=True, err=True, force=True)
            return False

        status = self._androidBooleanMethod(ANDROID_ADSERVICE_PLUGIN_NAME, "canOfferRewarded", placement)
        self.__logAd("[Rewarded] available to offer {} is {}".format(placement, status))
        return status

    def canYouShowRewardedAdvert(self, placement):
        if self.rewarded_inited is False:
            self.__logAd("ad canYouShowRewarded not inited", trace=True, err=True, force=True)
            return False

        status = self._androidBooleanMethod(ANDROID_ADSERVICE_PLUGIN_NAME, "canYouShowRewarded", placement)
        self.__logAd("[Rewarded] available to show {} is {}".format(placement, status))
        return status

    def showRewardedAdvert(self, placement):
        if self.rewarded_inited is False:
            self.__logAd("ad showRewarded not inited", trace=True, err=True, force=True)
            return False

        self.__logAd("[Rewarded] show {}".format(placement))
        return self._androidBooleanMethod(ANDROID_ADSERVICE_PLUGIN_NAME, "showRewarded", placement)

    def isShowingRewardedAdvert(self):
        if self.rewarded_inited is False:
            self.__logAd("ad isShowingRewarded not inited", trace=True, err=True, force=True)
            return False

        return self._androidBooleanMethod(ANDROID_ADSERVICE_PLUGIN_NAME, "isShowingRewarded")

    def _initializeBannerAd(self):
        if self.banner_inited is True:
            return True

        if Mengine.getConfigBool("Advertising", "Banner", False) is False:
            return False

        self.__logAd("[Banner] call init")
        self._addAndroidCallback(ANDROID_ADSERVICE_PLUGIN_NAME, "onAndroidAdServiceBannerRevenuePaid", self.__cbBannerRevenuePaid)
        self.banner_inited = True
        return True

    def _initializeInterstitialAd(self):
        if self.interstitial_inited is True:
            return True

        if Mengine.getConfigBool("Advertising", "Interstitial", False) is False:
            return False

        self.__logAd("[Interstitial] call init")
        self._addAndroidCallback(ANDROID_ADSERVICE_PLUGIN_NAME, "onAndroidAdServiceInterstitialShowSuccess", self.__cbInterstitialShowSuccess)
        self._addAndroidCallback(ANDROID_ADSERVICE_PLUGIN_NAME, "onAndroidAdServiceInterstitialShowFailed", self.__cbInterstitialShowFailed)
        self._addAndroidCallback(ANDROID_ADSERVICE_PLUGIN_NAME, "onAndroidAdServiceInterstitialRevenuePaid", self.__cbInterstitialRevenuePaid)
        self.interstitial_inited = True
        return True

    def _initializeRewardedAd(self):
        if self.rewarded_inited is True:
            return True

        if Mengine.getConfigBool("Advertising", "Rewarded", False) is False:
            return False

        self.__logAd("[Rewarded] call init")
        self._addAndroidCallback(ANDROID_ADSERVICE_PLUGIN_NAME, "onAndroidAdServiceRewardedShowSuccess", self.__cbRewardedShowSuccess)
        self._addAndroidCallback(ANDROID_ADSERVICE_PLUGIN_NAME, "onAndroidAdServiceRewardedShowFailed", self.__cbRewardedShowFailed)
        self._addAndroidCallback(ANDROID_ADSERVICE_PLUGIN_NAME, "onAndroidAdServiceRewardedUserRewarded", self.__cbRewardedUserRewarded)
        self._addAndroidCallback(ANDROID_ADSERVICE_PLUGIN_NAME, "onAndroidAdServiceRewardedRevenuePaid", self.__cbRewardedRevenuePaid)
        self.rewarded_inited = True
        return True

    def __cbBannerRevenuePaid(self, params):
        self.__logAd("[Banner cb] pay revenue {}".format(params))
        AdvertisementProvider.cbBannerRevenuePaid(params)

    def __cbInterstitialShowSuccess(self, params):
        self.__logAd("[Interstitial cb] show completed: True, params: {}".format(params))
        AdvertisementProvider.cbInterstitialShowCompleted(True, params)

    def __cbInterstitialShowFailed(self, params):
        self.__logAd("[Interstitial cb] show completed: False, params: {}".format(params))
        AdvertisementProvider.cbInterstitialShowCompleted(False, params)

    def __cbInterstitialRevenuePaid(self, params):
        self.__logAd("[Interstitial cb] pay revenue {}".format(params))
        AdvertisementProvider.cbInterstitialRevenuePaid(params)

    def __cbRewardedShowSuccess(self, params):
        self.__logAd("[Rewarded cb] show completed: True, params: {}".format(params))
        AdvertisementProvider.cbRewardedShowCompleted(True, params)

    def __cbRewardedShowFailed(self, params):
        self.__logAd("[Rewarded cb] show completed: False, params: {}".format(params))
        AdvertisementProvider.cbRewardedShowCompleted(False, params)

    def __cbRewardedUserRewarded(self, params):
        self.__logAd("[Rewarded cb] user rewarded: {}".format(params))
        AdvertisementProvider.cbRewardedUserRewarded(params)

    def __cbRewardedRevenuePaid(self, params):
        self.__logAd("[Rewarded cb] pay revenue {}".format(params))
        AdvertisementProvider.cbRewardedRevenuePaid(params)

    def __logAd(self, *args, **kwargs):
        _Log(*args, **kwargs)