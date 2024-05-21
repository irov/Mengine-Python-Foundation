from Foundation.Providers.BaseProvider import BaseProvider


class AdvertisementProvider(BaseProvider):
    """
    Types of Advertisement (AdType):
        - Rewarded
        - Interstitial
        - Banner
    """

    s_allowed_methods = [
        "ShowRewardedAdvert",
        "ShowInterstitialAdvert",
        "CanOfferRewardedAdvert",
        "CanOfferInterstitialAdvert",
        "IsRewardedAdvertAvailable",
        "IsInterstitialAdvertAvailable",
        "ShowBanner",
        "HideBanner",
        "ShowConsentFlow",
        "IsConsentFlow",
        "GetBannerViewport",
    ]

    @staticmethod
    def _setDevProvider():
        DummyAdvertisement.setProvider()

    @staticmethod
    def showAdvert(AdType, AdUnitName=None, **params):
        if AdUnitName is None:
            AdUnitName = AdType
        return AdvertisementProvider._call("Show{}Advert".format(AdType), AdUnitName, **params)

    @staticmethod
    def canOfferAdvert(AdType, AdUnitName=None, **params):
        if AdUnitName is None:
            AdUnitName = AdType
        return AdvertisementProvider._call("CanOffer{}Advert".format(AdType), AdUnitName, **params)

    @staticmethod
    def isAdvertAvailable(AdType, AdUnitName=None, **params):
        if AdUnitName is None:
            AdUnitName = AdType
        return AdvertisementProvider._call("Is{}AdvertAvailable".format(AdType), AdUnitName, **params)

    @staticmethod
    def showBanner(AdUnitName=None, **params):
        return AdvertisementProvider._call("ShowBanner", AdUnitName, **params)

    @staticmethod
    def hideBanner(AdUnitName=None, **params):
        return AdvertisementProvider._call("HideBanner", AdUnitName, **params)

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
    def getBannerViewport():
        return AdvertisementProvider._call("GetBannerViewport")


class DummyAdvertisement(object):
    """ Dummy Provider """

    @staticmethod
    def showAdvert(AdType, AdUnitName=None, **params):
        from Foundation.TaskManager import TaskManager

        DisplayFail = params.get("DisplayFail", "Random")
        FakeWatchDelay = params.get("Delay", 5000)
        GoldReward = params.get("GoldReward", 1)
        if AdUnitName is None:
            AdUnitName = params.get("AdUnitName", AdType)

        display_failed = Mengine.rand(20) < 5 if DisplayFail == "Random" else bool(DisplayFail)

        dummy_revenue = {
            "Banner": 0.005,
            "Rewarded": 0.05,
            "Interstitial": 0.02,
        }
        revenue = dummy_revenue[AdType]

        with TaskManager.createTaskChain(Name="DummyShow{}Advert".format(AdType)) as source:
            source.addPrint("<DummyAdvertisement> watch advertisement {}:{}, delay {}s (fail: {})...".format(
                AdType, AdUnitName, round(float(FakeWatchDelay) / 1000, 1), display_failed))

            if display_failed:
                source.addDelay(FakeWatchDelay)
                source.addNotify(Notificator.onAdvertDisplayFailed, AdType, AdUnitName)
            else:
                source.addNotify(Notificator.onAdvertDisplayed, AdType, AdUnitName)
                source.addDelay(FakeWatchDelay)

                if AdType == "Rewarded":
                    source.addNotify(Notificator.onAdvertRewarded, AdUnitName, "gold", GoldReward)

                source.addNotify(Notificator.onAdvertHidden, AdType, AdUnitName)
                source.addNotify(Notificator.onAdvertPayRevenue, AdType, AdUnitName, revenue)

    @staticmethod
    def canOfferAdvert(AdType, AdUnitName=None, **params):
        if AdUnitName is None:
            AdUnitName = AdType

        status = True
        if AdType == "Rewarded":
            status = Mengine.rand(20) < 15

        Trace.msg("<DummyAdvertisement> canOfferAdvert {}:{} result = {}".format(AdType, AdUnitName, status))
        return status

    @staticmethod
    def isAdvertAvailable(AdType, AdUnitName=None, **params):
        if AdUnitName is None:
            AdUnitName = AdType
        status = Mengine.rand(100) <= 90
        Trace.msg("<DummyAdvertisement> isAdvertAvailable {}:{} result = {}".format(AdType, AdUnitName, status))
        return status

    @staticmethod
    def showBanner(AdUnitName=None, **params):
        AdType = "Banner"
        if AdUnitName is None:
            AdUnitName = params.get("AdUnitName", AdType)

        DisplayFail = params.get("DisplayFail", "Random")

        display_failed = Mengine.rand(20) < 5 if DisplayFail == "Random" else bool(DisplayFail)

        Trace.msg("<DummyAdvertisement> show advert {}:{} (fail: {})...".format(
            AdType, AdUnitName, display_failed))

        if display_failed is True:
            Notification.notify(Notificator.onAdvertDisplayFailed, AdType, AdUnitName)
        else:
            Notification.notify(Notificator.onAdvertDisplayed, AdType, AdUnitName)

        return True

    @staticmethod
    def hideBanner(AdUnitName=None, **params):
        AdType = "Banner"
        if AdUnitName is None:
            AdUnitName = params.get("AdUnitName", AdType)

        Notification.notify(Notificator.onAdvertHidden, AdType, AdUnitName)

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
        def _ShowRewardedAdvert(AdUnitName=None, **_):
            return DummyAdvertisement.showAdvert("Rewarded", AdUnitName)
        def _CanOfferRewardedAdvert(AdUnitName=None, **_):
            return DummyAdvertisement.canOfferAdvert("Rewarded", AdUnitName)
        def _IsRewardedAdvertAvailable(AdUnitName=None, **_):
            return DummyAdvertisement.isAdvertAvailable("Rewarded", AdUnitName)
        def _ShowInterstitialAdvert(AdUnitName=None, **_):
            return DummyAdvertisement.showAdvert("Interstitial", AdUnitName)
        def _CanOfferInterstitialAdvert(AdUnitName=None, **_):
            return DummyAdvertisement.canOfferAdvert("Interstitial", AdUnitName)
        def _IsInterstitialAdvertAvailable(AdUnitName=None, **_):
            return DummyAdvertisement.isAdvertAvailable("Interstitial", AdUnitName)
        def _ShowBanner(AdUnitName=None, **_):
            return DummyAdvertisement.showBanner(AdUnitName)
        def _HideBanner(AdUnitName=None, **_):
            return DummyAdvertisement.hideBanner(AdUnitName)
        def _ShowConsentFlow():
            return DummyAdvertisement.showConsentFlow()
        def _IsConsentFlow():
            return DummyAdvertisement.isConsentFlow()

        methods = dict(
            # rewarded:
            ShowRewardedAdvert=_ShowRewardedAdvert,
            CanOfferRewardedAdvert=_CanOfferRewardedAdvert,
            IsRewardedAdvertAvailable=_IsRewardedAdvertAvailable,
            # interstitial:
            ShowInterstitialAdvert=_ShowInterstitialAdvert,
            CanOfferInterstitialAdvert=_CanOfferInterstitialAdvert,
            IsInterstitialAdvertAvailable=_IsInterstitialAdvertAvailable,
            # banner:
            ShowBanner=_ShowBanner,
            HideBanner=_HideBanner,
            # consent flow:
            ShowConsentFlow=_ShowConsentFlow,
            IsConsentFlow=_IsConsentFlow,
        )

        AdvertisementProvider.setProvider("Dummy", methods)
