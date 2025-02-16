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
        from Foundation.Providers.DummyAdvertisement import DummyAdvertisement
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
    def canYouShowInterstitialAdvert(placement):
        return AdvertisementProvider._call("CanYouShowInterstitialAdvert", placement)

    @staticmethod
    def showInterstitialAdvert(placement):
        return AdvertisementProvider._call("ShowInterstitialAdvert", placement)

    @staticmethod
    def hasRewardedAdvert():
        return AdvertisementProvider._call("HasRewardedAdvert")

    @staticmethod
    def canOfferRewardedAdvert(placement):
        return AdvertisementProvider._call("CanOfferRewardedAdvert", placement)

    @staticmethod
    def canYouShowRewardedAdvert(placement):
        return AdvertisementProvider._call("CanYouShowRewardedAdvert", placement)

    @staticmethod
    def showRewardedAdvert(placement):
        return AdvertisementProvider._call("ShowRewardedAdvert", placement)

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