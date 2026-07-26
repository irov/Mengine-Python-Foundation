from Foundation.Providers.AdvertisementProvider import AdvertisementProvider
from Foundation.System import System
from Foundation.Task.Semaphore import Semaphore
from Foundation.Utils import SimpleLogger

_Log = SimpleLogger("SystemAdService")


class SystemAppleAd(System):
    def __init__(self):
        super(SystemAppleAd, self).__init__()

        self.semaphoreAdServiceReady = Semaphore(False, "AdServiceReady")
        self.banner_inited = False
        self.interstitial_inited = False
        self.rewarded_inited = False

    def _onFinalize(self):
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
        return Mengine.iOSAdvertisementGetBannerWidth()

    def getBannerHeight(self):
        return Mengine.iOSAdvertisementGetBannerHeight()

    def getNoAds(self):
        return Mengine.iOSAdvertisementGetNoAds()

    def showBanner(self):
        if self.banner_inited is False:
            self.__logAd("ad showBanner not inited", trace=True, err=True, force=True)
            return False

        self.__logAd("[Banner] show banner")
        return Mengine.iOSAdvertisementShowBanner()

    def hideBanner(self):
        if self.banner_inited is False:
            self.__logAd("ad hideBanner not inited", trace=True, err=True, force=True)
            return False

        self.__logAd("[Banner] hide banner")
        return Mengine.iOSAdvertisementHideBanner()

    def hasInterstitialAdvert(self):
        return Mengine.iOSAdvertisementHasInterstitial()

    def canYouShowInterstitialAdvert(self, placement):
        if self.interstitial_inited is False:
            self.__logAd("ad canYouShowInterstitial not inited", trace=True, err=True, force=True)
            return False

        status = Mengine.iOSAdvertisementCanYouShowInterstitial(placement)
        self.__logAd("[Interstitial] available to show {} is {}".format(placement, status))
        return status

    def showInterstitialAdvert(self, placement):
        if self.interstitial_inited is False:
            self.__logAd("ad showInterstitial not inited", trace=True, err=True, force=True)
            return False

        self.__logAd("[Interstitial] show {}".format(placement))
        return Mengine.iOSAdvertisementShowInterstitial(placement)

    def isShowingInterstitialAdvert(self):
        if self.interstitial_inited is False:
            self.__logAd("ad isShowingInterstitial not inited", trace=True, err=True, force=True)
            return False

        return Mengine.iOSAdvertisementIsShowingInterstitial()

    def hasRewardedAdvert(self):
        return Mengine.iOSAdvertisementHasRewarded()

    def canOfferRewardedAdvert(self, placement):
        if self.rewarded_inited is False:
            self.__logAd("ad canOfferRewarded not inited", trace=True, err=True, force=True)
            return False

        status = Mengine.iOSAdvertisementCanOfferRewarded(placement)
        self.__logAd("[Rewarded] available to offer {} is {}".format(placement, status))
        return status

    def canYouShowRewardedAdvert(self, placement):
        if self.rewarded_inited is False:
            self.__logAd("ad canYouShowRewarded not inited", trace=True, err=True, force=True)
            return False

        status = Mengine.iOSAdvertisementCanYouShowRewarded(placement)
        self.__logAd("[Rewarded] available to show {} is {}".format(placement, status))
        return status

    def showRewardedAdvert(self, placement):
        if self.rewarded_inited is False:
            self.__logAd("ad showRewarded not inited", trace=True, err=True, force=True)
            return False

        self.__logAd("[Rewarded] show {}".format(placement))
        return Mengine.iOSAdvertisementShowRewarded(placement)

    def isShowingRewardedAdvert(self):
        if self.rewarded_inited is False:
            self.__logAd("ad isShowingRewarded not inited", trace=True, err=True, force=True)
            return False

        return Mengine.iOSAdvertisementIsShowingRewarded()

    def _initializeBannerAd(self):
        if self.banner_inited is True:
            return True

        if Mengine.getConfigBool("Advertising", "Banner", False) is False:
            return False

        self.__logAd("[Banner] call init")

        callbacks = {
            "oniOSAdvertisementRevenuePaid": self.__cbBannerRevenuePaid,
        }

        Mengine.iOSAdvertisementSetBannerCallback(callbacks)

        self.banner_inited = True
        return True

    def _initializeInterstitialAd(self):
        if self.interstitial_inited is True:
            return True

        if Mengine.getConfigBool("Advertising", "Interstitial", False) is False:
            return False

        self.__logAd("[Interstitial] call init")

        callbacks = {
            "oniOSAdvertisementShowSuccess": self.__cbInterstitialShowSuccess,
            "oniOSAdvertisementShowFailed": self.__cbInterstitialShowFailed,
            "oniOSAdvertisementRevenuePaid": self.__cbInterstitialRevenuePaid,
        }

        Mengine.iOSAdvertisementSetInterstitialCallback(callbacks)

        self.interstitial_inited = True
        return True

    def _initializeRewardedAd(self):
        if self.rewarded_inited is True:
            return True

        if Mengine.getConfigBool("Advertising", "Rewarded", False) is False:
            return False

        self.__logAd("[Rewarded] call init")

        callbacks = {
            "oniOSAdvertisementShowSuccess": self.__cbRewardedShowSuccess,
            "oniOSAdvertisementShowFailed": self.__cbRewardedShowFailed,
            "oniOSAdvertisementUserRewarded": self.__cbRewardedUserRewarded,
            "oniOSAdvertisementRevenuePaid": self.__cbRewardedRevenuePaid,
        }

        Mengine.iOSAdvertisementSetRewardedCallback(callbacks)

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
