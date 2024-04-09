from Foundation.Systems.AppLovin.AndroidInterstitialAd import AndroidInterstitialAd
from Foundation.Systems.AppLovin.AndroidRewardedAd import AndroidRewardedAd
from Foundation.Systems.AppLovin.AndroidBanner import AndroidBanner
from Foundation.Systems.AppLovin.IOSInterstitialAd import IOSInterstitialAd
from Foundation.Systems.AppLovin.IOSRewardedAd import IOSRewardedAd
from Foundation.Systems.AppLovin.IOSBanner import IOSBanner


class AppLovinAdFactory(object):

    @staticmethod
    def createAd(ad_type, ad_name):
        types = ("Interstitial", "Rewarded", "Banner")

        if ad_type not in types:
            Trace.log("System", 0, "Wrong ad_type {!r}, must be one of these: {}".format(ad_type, types))
            return None

        if _ANDROID is True:
            return AppLovinAdFactory._createAndroidAd(ad_type, ad_name)
        elif _IOS is True:
            return AppLovinAdFactory._createIOSAd(ad_type, ad_name)

        Trace.log("System", 0, "Wrong OS, must be Android or iOS")
        return None

    @staticmethod
    def _createAndroidAd(ad_type, ad_name):
        types = {
            "Interstitial": AndroidInterstitialAd,
            "Rewarded": AndroidRewardedAd,
            "Banner": AndroidBanner,
        }

        Type = types[ad_type]
        ad_unit = Type(ad_name)
        return ad_unit

    @staticmethod
    def _createIOSAd(ad_type, ad_name):
        types = {
            "Interstitial": IOSInterstitialAd,
            "Rewarded": IOSRewardedAd,
            "Banner": IOSBanner,
        }

        Type = types[ad_type]
        ad_unit = Type(ad_name)
        return ad_unit

