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
    def showAdvert(AdType, **params):
        """ type: Rewarded|Interstitial """
        return AdvertisementProvider._call("Show{}Advert".format(AdType), **params)

    @staticmethod
    def canOfferAdvert(AdType, **params):
        return AdvertisementProvider._call("CanOffer{}Advert".format(AdType), **params)

    @staticmethod
    def isAdvertAvailable(AdType, **params):
        return AdvertisementProvider._call("Is{}AdvertAvailable".format(AdType), **params)


class DummyAdvertisement(object):
    """ Dummy Provider """

    @staticmethod
    def showAdvert(AdType, **params):
        from Foundation.TaskManager import TaskManager

        DisplayFail = params.get("DisplayFail", "Random")
        FakeWatchDelay = params.get("Delay", 5000)
        GoldReward = params.get("GoldReward", 1)

        display_failed = Mengine.rand(20) < 5 if DisplayFail is "Random" else bool(DisplayFail)

        with TaskManager.createTaskChain(Name="DummyShow{}Advert".format(AdType)) as source:
            source.addPrint("<DummyAdvertisement> watch advertisement, delay {}s (display failed is {})...".format(round(float(FakeWatchDelay) / 1000, 1), display_failed))

            if display_failed:
                source.addDelay(FakeWatchDelay)
                source.addNotify(Notificator.onAdvertDisplayFailed, AdType)
            else:
                source.addNotify(Notificator.onAdvertDisplayed, AdType)
                source.addDelay(FakeWatchDelay)

                if AdType == "Rewarded":
                    source.addNotify(Notificator.onAdvertRewarded, "gold", GoldReward)

                source.addNotify(Notificator.onAdvertHidden, AdType)

    @staticmethod
    def canOfferAdvert(AdType, **params):
        if AdType == "Rewarded":
            status = Mengine.rand(20) < 15
            return status
        return True

    @staticmethod
    def isAdvertAvailable(AdType, **params):
        return True

    @staticmethod
    def setProvider():
        methods = dict()

        for AdType in ["Interstitial", "Rewarded"]:
            ad_type_methods = {
                "Show{}Advert".format(AdType): lambda: DummyAdvertisement.showAdvert(AdType),
                "CanOffer{}Advert".format(AdType): lambda: DummyAdvertisement.canOfferAdvert(AdType),
                "Is{}AdvertAvailable".format(AdType): lambda: DummyAdvertisement.isAdvertAvailable(AdType),
            }
            methods.update(ad_type_methods)

        AdvertisementProvider.setProvider("Dummy", methods)
