from Foundation.Providers.BaseProvider import BaseProvider


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
    def hasAdvert(AdType, placement):
        status = True

        Trace.msg("<DummyAdvertisement> hasAdvert {}:{} result = {}".format(AdType, placement, status))
        return status

    @staticmethod
    def showAdvert(AdType, placement):
        from Foundation.TaskManager import TaskManager

        DisplayFail = params.get("DisplayFail", "Random")
        FakeWatchDelay = params.get("Delay", 5000)
        GoldReward = params.get("GoldReward", 1)

        display_failed = Mengine.rand(20) < 5 if DisplayFail == "Random" else bool(DisplayFail)

        dummy_revenue = {
            "Banner": 0.005,
            "Rewarded": 0.05,
            "Interstitial": 0.02,
        }
        revenue = dummy_revenue[AdType]

        with TaskManager.createTaskChain(Name="DummyShow{}Advert".format(AdType)) as source:
            source.addPrint("<DummyAdvertisement> watch advertisement {}:{}, delay {}s (fail: {})...".format(
                AdType, placement, round(float(FakeWatchDelay) / 1000, 1), display_failed))

            if display_failed:
                source.addDelay(FakeWatchDelay)
                source.addNotify(Notificator.onAdShowCompleted, AdType, False, {"placement": placement})
            else:
                source.addDelay(FakeWatchDelay)

                if AdType == "Rewarded":
                    source.addNotify(Notificator.onAdUserRewarded, placement, {"gold": GoldReward})

                source.addNotify(Notificator.onAdShowCompleted, AdType, True, {"placement": placement})
                source.addNotify(Notificator.onAdRevenuePaid, AdType, {"placement": placement, "revenue": revenue})

    @staticmethod
    def canOfferAdvert(AdType, placement):
        status = True
        if AdType == "Rewarded":
            status = Mengine.rand(20) < 15

        Trace.msg("<DummyAdvertisement> canOfferAdvert {}:{} result = {}".format(AdType, placement, status))
        return status

    @staticmethod
    def сanYouShowAdvert(AdType, placement):
        status = Mengine.rand(100) <= 90
        Trace.msg("<DummyAdvertisement> isAdvertAvailable {}:{} result = {}".format(AdType, placement, status))
        return status

    @staticmethod
    def showBanner():
        AdType = "Banner"

        DisplayFail = params.get("DisplayFail", "Random")

        display_failed = Mengine.rand(20) < 5 if DisplayFail == "Random" else bool(DisplayFail)

        Trace.msg("<DummyAdvertisement> show advert {} (fail: {})...".format(
            AdType, display_failed))

        return True

    @staticmethod
    def hideBanner():
        AdType = "Banner"

        Notification.notify(Notificator.onAdShowCompleted, AdType, True, {})

        return True

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
            return DummyAdvertisement.hasAdvert("Rewarded", placement)
        def _HasInterstitialAdvert(placement):
            return DummyAdvertisement.hasAdvert("Interstitial", placement)
        def _ShowRewardedAdvert(placement):
            return DummyAdvertisement.showAdvert("Rewarded", placement)
        def _CanOfferRewardedAdvert(placement):
            return DummyAdvertisement.canOfferAdvert("Rewarded", placement)
        def _CanYouShowRewardedAdvert(placement):
            return DummyAdvertisement.сanYouShowAdvert("Rewarded", placement)
        def _ShowInterstitialAdvert(placement):
            return DummyAdvertisement.showAdvert("Interstitial", placement)
        def _CanOfferInterstitialAdvert(placement):
            return DummyAdvertisement.canOfferAdvert("Interstitial", placement)
        def _CanYouShowInterstitialAdvert(placement):
            return DummyAdvertisement.сanYouShowAdvert("Interstitial", placement)
        def _ShowBanner(placement):
            return DummyAdvertisement.showBanner(placement)
        def _HideBanner(placement):
            return DummyAdvertisement.hideBanner(placement)
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
            CanOfferInterstitialAdvert=_CanOfferInterstitialAdvert,
            CanYouShowInterstitialAdvert=_CanYouShowInterstitialAdvert,
            # banner:
            ShowBanner=_ShowBanner,
            HideBanner=_HideBanner,
            # consent flow:
            ShowConsentFlow=_ShowConsentFlow,
            IsConsentFlow=_IsConsentFlow,
        )

        AdvertisementProvider.setProvider("Dummy", methods)
