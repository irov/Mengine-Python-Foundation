from Foundation.Systems.AppLovin.BaseAdUnit import BaseAdUnit

class IOSRewardedAd(BaseAdUnit):
    ad_type = "Rewarded"

    def _initialize(self):
        callbacks = {
            "onAppleAdvertisementShowSuccess": self.cbShowSuccess,
            "onAppleAdvertisementShowFailed": self.cbShowFailed,
            "onAppleAdvertisementUserRewarded": self.cbUserRewarded,
            "onAppleAdvertisementRevenuePaid": self.cbRevenuePaid,
        }

        return Mengine.appleAdvertisementSetRewardedCallback(callbacks)

    def _has(self):
        return Mengine.appleAdvertisementHasRewarded()

    def _canOffer(self, placement):
        return Mengine.appleAdvertisementCanOfferRewarded(placement)

    def _canYouShow(self, placement):
        return Mengine.appleAdvertisementCanYouShowRewarded(placement)

    def _show(self, placement):
        return Mengine.appleAdvertisementShowRewarded(placement)
