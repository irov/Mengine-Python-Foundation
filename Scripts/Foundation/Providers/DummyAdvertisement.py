from Foundation.Providers.AdvertisementProvider import AdvertisementProvider
from Foundation.TaskManager import TaskManager


class DummyAdvertisement(object):
    """ Dummy Provider """

# ----- Banner ---------------------------------------------------------------------------------------------------------

    @staticmethod
    def showBanner():
        AdType = "Banner"
        display_failed = Mengine.rand(20) < 5
        Trace.msg("<DummyAdvertisement> show advert {} (fail: {})...".format(AdType, display_failed))
        return True

    @staticmethod
    def hideBanner():
        AdType = "Banner"
        Notification.notify(Notificator.onAdShowCompleted, AdType, True, {})
        return True

    @staticmethod
    def getBannerHeight():
        viewport = Mengine.getGameViewport()
        game_width = viewport.end.x - viewport.begin.x
        game_height = viewport.end.y - viewport.begin.y

        if Utils.isTabletByAspectRatio(game_width, game_height) is True:
            banner_height = DummyAdvertisement.getTabletAdaptiveBannerHeight(game_width)
        else:
            banner_height = DummyAdvertisement.getPhoneAdaptiveBannerHeight(game_width)

        return banner_height

    @staticmethod
    def getBannerWidth():
        viewport = Mengine.getGameViewport()
        game_width = viewport.end.x - viewport.begin.x
        return game_width

    @staticmethod
    def getPhoneAdaptiveBannerHeight(width):
        """ Applovin Banners are automatically sized to 320x50 on phones """
        return 50.0 * width / 320.0

    @staticmethod
    def getTabletAdaptiveBannerHeight(width):
        """ Applovin Banners are automatically sized to 728x90 on tablets """
        return 90.0 * width / 728.0

# ----------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def hasInterstitialAdvert():
        status = True
        Trace.msg("<DummyAdvertisement> hasInterstitialAdvert result = {}".format(status))
        return status

    @staticmethod
    def canYouShowInterstitialAdvert(placement):
        status = Mengine.rand(100) <= 90
        Trace.msg("<DummyAdvertisement> canYouShowInterstitialAdvert {} result = {}".format(placement, status))
        return status

    @staticmethod
    def showInterstitialAdvert(placement):
        FakeWatchDelay = 5000
        display_failed = Mengine.rand(20) < 5
        revenue = 0.02

        with TaskManager.createTaskChain(Name="DummyShowInterstitialAdvert") as source:
            source.addPrint("<DummyAdvertisement> watch showInterstitialAdvert {}, delay {}s (fail: {})...".format(
                placement, round(float(FakeWatchDelay) / 1000, 1), display_failed))

            if display_failed:
                source.addDelay(FakeWatchDelay)
                source.addNotify(Notificator.onAdShowCompleted, "Interstitial", False, {"placement": placement})
            else:
                source.addDelay(FakeWatchDelay)

                source.addNotify(Notificator.onAdShowCompleted, "Interstitial", True, {"placement": placement})
                source.addNotify(Notificator.onAdRevenuePaid, "Interstitial", {"placement": placement, "revenue": revenue})

        return True

    @staticmethod
    def hasRewardedAdvert():
        status = True
        Trace.msg("<DummyAdvertisement> hasRewardedAdvert result = {}".format(status))
        return status

    @staticmethod
    def canOfferRewardedAdvert(placement):
        status = Mengine.rand(20) < 15
        Trace.msg("<DummyAdvertisement> canOfferRewardedAdvert {} result = {}".format(placement, status))
        return status

    @staticmethod
    def canYouShowRewardedAdvert(placement):
        status = Mengine.rand(100) <= 90
        Trace.msg("<DummyAdvertisement> canYouShowRewardedAdvert {} result = {}".format(placement, status))
        return status

    @staticmethod
    def showRewardedAdvert(placement):
        FakeWatchDelay = 5000
        GoldReward = 1
        display_failed = Mengine.rand(20) < 5
        revenue = 0.05

        with TaskManager.createTaskChain(Name="DummyShowRewardedAdvert") as source:
            source.addPrint("<DummyAdvertisement> watch showRewardedAdvert {}, delay {}s (fail: {})...".format(
                placement, round(float(FakeWatchDelay) / 1000, 1), display_failed))

            if display_failed:
                source.addDelay(FakeWatchDelay)
                source.addNotify(Notificator.onAdShowCompleted, "Rewarded", False, {"placement": placement})
            else:
                source.addDelay(FakeWatchDelay)

                source.addNotify(Notificator.onAdUserRewarded, "Rewarded", {"placement": placement})

                source.addNotify(Notificator.onAdShowCompleted, "Rewarded", True, {"placement": placement})
                source.addNotify(Notificator.onAdRevenuePaid, "Rewarded", {"placement": placement, "revenue": revenue})

    @staticmethod
    def showConsentFlow():
        Trace.msg("<DummyAdvertisement> DUMMY show consent flow...")
        return

    @staticmethod
    def isConsentFlow():
        return Mengine.getConfigBool("Advertising", "DummyConsentFlow", False) is True

    @staticmethod
    def setProvider():
        def _HasRewardedAdvert():
            return DummyAdvertisement.hasRewardedAdvert()
        def _HasInterstitialAdvert():
            return DummyAdvertisement.hasInterstitialAdvert()
        def _ShowRewardedAdvert(placement):
            return DummyAdvertisement.showRewardedAdvert(placement)
        def _CanOfferRewardedAdvert(placement):
            return DummyAdvertisement.canOfferRewardedAdvert(placement)
        def _CanYouShowRewardedAdvert(placement):
            return DummyAdvertisement.canYouShowRewardedAdvert(placement)
        def _ShowInterstitialAdvert(placement):
            return DummyAdvertisement.showInterstitialAdvert(placement)
        def _IsShowingInterstitialAdvert():
            return False
        def _IsShowingRewardedAdvert():
            return False
        def _CanYouShowInterstitialAdvert(placement):
            return DummyAdvertisement.canYouShowInterstitialAdvert(placement)
        def _ShowBanner():
            return DummyAdvertisement.showBanner()
        def _HideBanner():
            return DummyAdvertisement.hideBanner()
        def _GetBannerHeight():
            return DummyAdvertisement.getBannerHeight()
        def _GetBannerWidth():
            return DummyAdvertisement.getBannerWidth()
        def _ShowConsentFlow():
            return DummyAdvertisement.showConsentFlow()
        def _IsConsentFlow():
            return DummyAdvertisement.isConsentFlow()

        methods = dict(
            # banner:
            ShowBanner=_ShowBanner,
            HideBanner=_HideBanner,
            GetBannerHeight=_GetBannerHeight,
            GetBannerWidth=_GetBannerWidth,
            # interstitial:
            HasInterstitialAdvert=_HasInterstitialAdvert,
            CanYouShowInterstitialAdvert=_CanYouShowInterstitialAdvert,
            ShowInterstitialAdvert=_ShowInterstitialAdvert,
            IsShowingInterstitialAdvert=_IsShowingInterstitialAdvert,
            # rewarded:
            HasRewardedAdvert=_HasRewardedAdvert,
            CanOfferRewardedAdvert=_CanOfferRewardedAdvert,
            CanYouShowRewardedAdvert=_CanYouShowRewardedAdvert,
            ShowRewardedAdvert=_ShowRewardedAdvert,
            IsShowingRewardedAdvert=_IsShowingRewardedAdvert,
            # consent flow:
            ShowConsentFlow=_ShowConsentFlow,
            IsConsentFlow=_IsConsentFlow,
        )

        AdvertisementProvider.setProvider("Dummy", methods)
