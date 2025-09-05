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
        "IsShowingInterstitialAdvert",
        "HasRewardedAdvert",
        "CanOfferRewardedAdvert",
        "CanYouShowRewardedAdvert",
        "ShowRewardedAdvert",
        "IsShowingRewardedAdvert",
        "ShowConsentFlow",
        "IsConsentFlow",
        "GetBannerHeight",
        "GetBannerWidth",
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
    def isShowingInterstitialAdvert():
        return AdvertisementProvider._call("IsShowingInterstitialAdvert")

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

    @staticmethod
    def isShowingRewardedAdvert():
        return AdvertisementProvider._call("IsShowingRewardedAdvert")

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

    @staticmethod
    def getBannerWidth():
        return AdvertisementProvider._call("GetBannerWidth")
