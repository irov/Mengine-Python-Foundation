from Foundation.Providers.BaseProvider import BaseProvider


class AdvertisementProvider(BaseProvider):
    """
    Types of Advertisement (AdType):
        - Rewarded
        - Interstitial
    """

    s_allowed_methods = [
        "ShowRewardedAdvert",
        "ShowInterstitialAdvert",
        "CanOfferRewardedAdvert",
        "CanOfferInterstitialAdvert",
        "IsRewardedAdvertAvailable",
        "IsInterstitialAdvertAvailable",
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

        display_failed = Mengine.rand(20) < 5 if DisplayFail is "Random" else bool(DisplayFail)

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
        status = True
        Trace.msg("<DummyAdvertisement> isAdvertAvailable {}:{} result = {}".format(AdType, AdUnitName, status))
        return status

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

        methods = dict(
            # rewarded:
            ShowRewardedAdvert=_ShowRewardedAdvert,
            CanOfferRewardedAdvert=_CanOfferRewardedAdvert,
            IsRewardedAdvertAvailable=_IsRewardedAdvertAvailable,
            # interstitial:
            ShowInterstitialAdvert=_ShowInterstitialAdvert,
            CanOfferInterstitialAdvert=_CanOfferInterstitialAdvert,
            IsInterstitialAdvertAvailable=_IsInterstitialAdvertAvailable,
        )

        AdvertisementProvider.setProvider("Dummy", methods)
