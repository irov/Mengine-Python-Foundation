class AdvertisementProvider(object):
    """
    Types of Advertisement (AdType):
        - Rewarded
        - Interstitial

    Names:
        - Show{AdType}Advert
        - CanOffer{AdType}Advert
        - Is{AdType}AdvertAvailable
    """

    s_name = None
    s_methods = {}

    @staticmethod
    def setProvider(name, methods):
        if isinstance(methods, dict) is False:
            Trace.log("Provider", 0, "Wrong type {} must be dict".format(type(methods)))
            return False

        AdvertisementProvider.s_methods = methods
        AdvertisementProvider.s_name = name

        return True

    @staticmethod
    def setDevProvider():
        if _DEVELOPMENT is False:
            return

        DummyAdvertisement.setProvider()

    @staticmethod
    def getName():
        return AdvertisementProvider.s_name

    @staticmethod
    def removeProvider():
        AdvertisementProvider.s_name = None
        AdvertisementProvider.s_methods = {}

    # -------- Interface ---------------------------------------------------------------------------------------------------

    @staticmethod
    def showAdvert(AdType, **params):
        """ type: Rewarded|Interstitial """
        fn = AdvertisementProvider.s_methods.get("Show{}Advert".format(AdType))

        if fn is None:
            Trace.log("Provider", 1, "Not found method for ad {}".format(AdType))
            return False

        return fn(**params)

    @staticmethod
    def canOfferAdvert(AdType, **params):
        fn = AdvertisementProvider.s_methods.get("CanOffer{}Advert".format(AdType))

        if fn is None:
            Trace.log("Provider", 1, "Not found method for ad {}".format(AdType))
            return False

        return fn(**params)

    @staticmethod
    def isAdvertAvailable(AdType, **params):
        fn = AdvertisementProvider.s_methods.get("Is{}AdvertAvailable".format(AdType))

        if fn is None:
            Trace.log("Provider", 1, "Not found method for ad {}".format(AdType))
            return False

        return fn(**params)

class DummyAdvertisement(object):
    """ Dummy Provider """

    @staticmethod
    def showAdvert(AdType, **params):
        from Foundation.TaskManager import TaskManager

        DisplayFail = params.get("DisplayFail", "Random")
        FakeWatchDelay = params.get("Delay", 1500)
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
            ad_type_methods = {"Show{}Advert".format(AdType): lambda: DummyAdvertisement.showAdvert(AdType), "CanOffer{}Advert".format(AdType): lambda: DummyAdvertisement.canOfferAdvert(AdType), "Is{}AdvertAvailable".format(AdType): lambda: DummyAdvertisement.isAdvertAvailable(AdType), }
            methods.update(ad_type_methods)

        AdvertisementProvider.setProvider("Dummy", methods)