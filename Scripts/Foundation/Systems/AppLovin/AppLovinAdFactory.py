from Foundation.Systems.AppLovin.AndroidAppLovinInterstitialAd import AndroidAppLovinInterstitialAd
from Foundation.Systems.AppLovin.AndroidAppLovinRewardedAd import AndroidAppLovinRewardedAd
from Foundation.Systems.AppLovin.AndroidAppLovinBannerAd import AndroidAppLovinBannerAd
from Foundation.Systems.AppLovin.IOSInterstitialAd import IOSInterstitialAd
from Foundation.Systems.AppLovin.IOSRewardedAd import IOSRewardedAd
from Foundation.Systems.AppLovin.IOSBanner import IOSBanner


class AppLovinAdFactory(object):

    @staticmethod
    def createAd(ad_type):
        types = ("Interstitial", "Rewarded", "Banner")

        if ad_type not in types:
            Trace.log("System", 0, "Wrong ad_type {!r}, must be one of these: {}".format(ad_type, types))
            return None

        if _ANDROID is True:
            return AppLovinAdFactory._createAndroidAd(ad_type)
        elif _IOS is True:
            return AppLovinAdFactory._createIOSAd(ad_type)

        Trace.log("System", 0, "Wrong OS, must be Android or iOS")
        return None

    @staticmethod
    def _createAndroidAd(ad_type):
        types = {
            "Interstitial": AndroidAppLovinInterstitialAd,
            "Rewarded": AndroidAppLovinRewardedAd,
            "Banner": AndroidAppLovinBannerAd,
        }

        Type = types[ad_type]
        ad_unit = Type()
        return ad_unit

    @staticmethod
    def _createIOSAd(ad_type):
        types = {
            "Interstitial": IOSInterstitialAd,
            "Rewarded": IOSRewardedAd,
            "Banner": IOSBanner,
        }

        Type = types[ad_type]
        ad_unit = Type()
        return ad_unit

