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
        "GetBannerHeight",
        "GetBannerWidth",
        "GetNoAds",
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

    @staticmethod
    def getBannerWidth():
        return AdvertisementProvider._call("GetBannerWidth")

    @staticmethod
    def getBannerHeight():
        return AdvertisementProvider._call("GetBannerHeight")

    @staticmethod
    def getNoAds():
        return AdvertisementProvider._call("GetNoAds")

    # --- Callbacks: must be invoked by concrete ad systems (Apple/Android/Dummy) -------------------------------------

    @staticmethod
    def cbBannerRevenuePaid(params):
        Notification.notify(Notificator.onBannerAdRevenuePaid, params)
        Notification.notify(Notificator.onAdRevenuePaid, "Banner", params)

    @staticmethod
    def cbInterstitialShowCompleted(success, params):
        Notification.notify(Notificator.onInterstitialAdShowCompleted, success, params)
        Notification.notify(Notificator.onAdShowCompleted, "Interstitial", success, params)

    @staticmethod
    def cbInterstitialRevenuePaid(params):
        Notification.notify(Notificator.onInterstitialAdRevenuePaid, params)
        Notification.notify(Notificator.onAdRevenuePaid, "Interstitial", params)

    @staticmethod
    def cbRewardedShowCompleted(success, params):
        Notification.notify(Notificator.onRewardedAdShowCompleted, success, params)
        Notification.notify(Notificator.onAdShowCompleted, "Rewarded", success, params)

    @staticmethod
    def cbRewardedUserRewarded(params):
        Notification.notify(Notificator.onRewardedAdUserRewarded, params)
        Notification.notify(Notificator.onAdUserRewarded, "Rewarded", params)

    @staticmethod
    def cbRewardedRevenuePaid(params):
        Notification.notify(Notificator.onRewardedAdRevenuePaid, params)
        Notification.notify(Notificator.onAdRevenuePaid, "Rewarded", params)