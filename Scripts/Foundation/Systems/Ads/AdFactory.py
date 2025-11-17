from Foundation.Systems.Ads.AndroidInterstitialAd import AndroidInterstitialAd
from Foundation.Systems.Ads.AndroidRewardedAd import AndroidRewardedAd
from Foundation.Systems.Ads.AndroidBannerAd import AndroidBannerAd
from Foundation.Systems.Ads.IOSInterstitialAd import IOSInterstitialAd
from Foundation.Systems.Ads.IOSRewardedAd import IOSRewardedAd
from Foundation.Systems.Ads.IOSBanner import IOSBannerAd

class AdFactory(object):
    @staticmethod
    def createAd(ad_type):
        types = ("Interstitial", "Rewarded", "Banner")

        if ad_type not in types:
            Trace.log("System", 0, "Wrong ad_type {!r}, must be one of these: {}".format(ad_type, types))
            return None

        if _ANDROID is True:
            return AdFactory._createAndroidAd(ad_type)
        elif _IOS is True:
            return AdFactory._createIOSAd(ad_type)

        Trace.log("System", 0, "Wrong OS, must be Android or iOS")
        return None

    @staticmethod
    def _createAndroidAd(ad_type):
        types = {
            "Interstitial": AndroidInterstitialAd,
            "Rewarded": AndroidRewardedAd,
            "Banner": AndroidBannerAd,
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

