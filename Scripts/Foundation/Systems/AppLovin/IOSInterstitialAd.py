from Foundation.Systems.AppLovin.BaseAdUnit import BaseAdUnit


class IOSInterstitialAd(BaseAdUnit):
    ad_type = "Interstitial"

    def _initialize(self):
        callbacks = {
            "onAppleAdvertisementShowSuccess": self.cbShowSuccess,
            "onAppleAdvertisementShowFailed": self.cbShowFailed,
            "onAppleAdvertisementRevenuePaid": self.cbRevenuePaid
        }

        return Mengine.appleAdvertisementSetAdvertisementInterstitialCallback(callbacks)

    def _has(self):
        return Mengine.appleAdvertisementHasInterstitial()

    def _canYouShow(self, placement):
        return Mengine.appleAdvertisementCanYouShowInterstitial(placement)

    def _show(self, placement):
        return Mengine.appleAdvertisementShowInterstitial(placement)
