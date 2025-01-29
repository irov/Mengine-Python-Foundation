from Foundation.Providers.BaseProvider import BaseProvider
from Foundation.TaskManager import TaskManager

class AdvertisementProvider(BaseProvider):
    """
    Types of Advertisement (AdType):
        - Rewarded
        - Interstitial
        - Banner
    """

    s_allowed_methods = [
        "ShowBanner",
        "HideBanner",
        "HasInterstitialAdvert",
        "CanYouShowInterstitialAdvert",
        "ShowInterstitialAdvert",
        "HasRewardedAdvert",
        "CanOfferRewardedAdvert",
        "CanYouShowRewardedAdvert",
        "ShowRewardedAdvert",
        "ShowConsentFlow",
        "IsConsentFlow",
        "GetBannerHeight",
    ]

    @staticmethod
    def _setDevProvider():
        DummyAdvertisement.setProvider()

    @staticmethod
    def showBanner():
        return AdvertisementProvider._call("ShowBanner")

    @staticmethod
    def hideBanner():
        return AdvertisementProvider._call("HideBanner")

    @staticmethod
    def hasInterstitialAdvert():
        return AdvertisementProvider._call("HasInterstitialAdvert")

    @staticmethod
    def canYouShowInterstitialAdvert(AdPlacement):
        return AdvertisementProvider._call("CanYouShowInterstitialAdvert", AdPlacement)

    @staticmethod
    def showInterstitialAdvert(AdPlacement):
        return AdvertisementProvider._call("ShowInterstitialAdvert", AdPlacement)

    @staticmethod
    def hasRewardedAdvert():
        return AdvertisementProvider._call("HasRewardedAdvert")

    @staticmethod
    def canOfferRewardedAdvert(AdPlacement):
        return AdvertisementProvider._call("CanOfferRewardedAdvert", AdPlacement)

    @staticmethod
    def canYouShowRewardedAdvert(AdPlacement):
        return AdvertisementProvider._call("CanYouShowRewardedAdvert", AdPlacement)

    @staticmethod
    def showRewardedAdvert(AdPlacement):
        return AdvertisementProvider._call("ShowRewardedAdvert", AdPlacement)

    # GDPR

    @staticmethod
    def showConsentFlow():
        return AdvertisementProvider._call("ShowConsentFlow")

    @staticmethod
    def isConsentFlow():
        return AdvertisementProvider._call("IsConsentFlow")

    @staticmethod
    def _isConsentFlowNotFoundCb():
        return False

    # OTHER

    @staticmethod
    def getBannerHeight():
        return AdvertisementProvider._call("GetBannerHeight")


class DummyAdvertisement(object):
    """ Dummy Provider """

    @staticmethod
    def showBanner():
        AdType = "Banner"

        display_failed = Mengine.rand(20) < 5

        Trace.msg("<DummyAdvertisement> show advert {} (fail: {})...".format(
            AdType, display_failed))

        return True

    @staticmethod
    def hideBanner():
        AdType = "Banner"

        Notification.notify(Notificator.onAdShowCompleted, AdType, True, {})

        return True

    @staticmethod
    def hasInterstitialAdvert(AdPlacement):
        status = True

        Trace.msg("<DummyAdvertisement> hasInterstitialAdvert {} result = {}".format(AdPlacement, status))
        return status

    @staticmethod
    def canYouShowInterstitialAdvert(AdPlacement):
        status = Mengine.rand(100) <= 90
        Trace.msg("<DummyAdvertisement> canYouShowInterstitialAdvert {} result = {}".format(AdPlacement, status))
        return status

    @staticmethod
    def showInterstitialAdvert(AdPlacement):
        FakeWatchDelay = 5000

        display_failed = Mengine.rand(20) < 5

        revenue = 0.02

        with TaskManager.createTaskChain(Name="DummyShowInterstitialAdvert") as source:
            source.addPrint("<DummyAdvertisement> watch showInterstitialAdvert {}, delay {}s (fail: {})...".format(
                AdPlacement, round(float(FakeWatchDelay) / 1000, 1), display_failed))

            if display_failed:
                source.addDelay(FakeWatchDelay)
                source.addNotify(Notificator.onAdShowCompleted, "Interstitial", False, {"placement": AdPlacement})
            else:
                source.addDelay(FakeWatchDelay)

                source.addNotify(Notificator.onAdShowCompleted, "Interstitial", True, {"placement": AdPlacement})
                source.addNotify(Notificator.onAdRevenuePaid, "Interstitial", {"placement": AdPlacement, "revenue": revenue})

    @staticmethod
    def canOfferRewardedAdvert(AdPlacement):
        status = Mengine.rand(20) < 15

        Trace.msg("<DummyAdvertisement> canOfferRewardedAdvert {} result = {}".format(AdPlacement, status))
        return status

    @staticmethod
    def canYouShowRewardedAdvert(AdPlacement):
        status = Mengine.rand(100) <= 90
        Trace.msg("<DummyAdvertisement> canYouShowRewardedAdvert {} result = {}".format(AdPlacement, status))
        return status

    @staticmethod
    def showRewardedAdvert(AdPlacement):
        FakeWatchDelay = 5000
        GoldReward = 1

        display_failed = Mengine.rand(20) < 5

        revenue = 0.05

        with TaskManager.createTaskChain(Name="DummyShowRewardedAdvert") as source:
            source.addPrint("<DummyAdvertisement> watch showRewardedAdvert {}, delay {}s (fail: {})...".format(
                AdPlacement, round(float(FakeWatchDelay) / 1000, 1), display_failed))

            if display_failed:
                source.addDelay(FakeWatchDelay)
                source.addNotify(Notificator.onAdShowCompleted, "Rewarded", False, {"placement": AdPlacement})
            else:
                source.addDelay(FakeWatchDelay)

                source.addNotify(Notificator.onAdUserRewarded, AdPlacement, {"gold": GoldReward})

                source.addNotify(Notificator.onAdShowCompleted, "Rewarded", True, {"placement": AdPlacement})
                source.addNotify(Notificator.onAdRevenuePaid, "Rewarded", {"placement": AdPlacement, "revenue": revenue})

    @staticmethod
    def showConsentFlow():
        Trace.msg("<DummyAdvertisement> DUMMY show consent flow...")
        return

    @staticmethod
    def isConsentFlow():
        return Mengine.getConfigBool("Advertising", "DummyConsentFlow", False) is True

    @staticmethod
    def setProvider():
        def _HasRewardedAdvert(placement):
            return DummyAdvertisement.hasRewardedAdvert(placement)
        def _HasInterstitialAdvert(placement):
            return DummyAdvertisement.hasInterstitialAdvert(placement)
        def _ShowRewardedAdvert(placement):
            return DummyAdvertisement.showRewardedAdvert(placement)
        def _CanOfferRewardedAdvert(placement):
            return DummyAdvertisement.canOfferRewardedAdvert(placement)
        def _CanYouShowRewardedAdvert(placement):
            return DummyAdvertisement.canYouShowRewardedAdvert(placement)
        def _ShowInterstitialAdvert(placement):
            return DummyAdvertisement.showInterstitialAdvert(placement)
        def _CanYouShowInterstitialAdvert(placement):
            return DummyAdvertisement.canYouShowInterstitialAdvert(placement)
        def _ShowBanner():
            return DummyAdvertisement.showBanner()
        def _HideBanner():
            return DummyAdvertisement.hideBanner()
        def _ShowConsentFlow():
            return DummyAdvertisement.showConsentFlow()
        def _IsConsentFlow():
            return DummyAdvertisement.isConsentFlow()

        methods = dict(
            # rewarded:
            HasRewardedAdvert=_HasRewardedAdvert,
            ShowRewardedAdvert=_ShowRewardedAdvert,
            CanOfferRewardedAdvert=_CanOfferRewardedAdvert,
            CanYouShowRewardedAdvert=_CanYouShowRewardedAdvert,
            # interstitial:
            HasInterstitialAdvert=_HasInterstitialAdvert,
            ShowInterstitialAdvert=_ShowInterstitialAdvert,
            CanYouShowInterstitialAdvert=_CanYouShowInterstitialAdvert,
            # banner:
            ShowBanner=_ShowBanner,
            HideBanner=_HideBanner,
            # consent flow:
            ShowConsentFlow=_ShowConsentFlow,
            IsConsentFlow=_IsConsentFlow,
        )

        AdvertisementProvider.setProvider("Dummy", methods)
