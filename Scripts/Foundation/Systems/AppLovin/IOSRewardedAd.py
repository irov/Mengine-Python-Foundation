from Foundation.Systems.AppLovin.BaseAdUnit import BaseAdUnit

class IOSRewardedAd(BaseAdUnit):
    ad_type = "Rewarded"

    def _initialize(self):
        callbacks = {
            "onAppleAppLovinRewardedShowSuccessful": self.cbShowSuccessful,
            "onAppleAppLovinRewardedShowFailed": self.cbShowFailed,
            "onAppleAppLovinRewardedUserRewarded": self.cbUserRewarded,
            "onAppleAppLovinRewardedRevenuePaid": self.cbRevenuePaid,
        }
        return Mengine.appleAppLovinSetRewardedProvider(callbacks)

    def _has(self):
        return Mengine.appleAppLovinHasRewarded()

    def _canOffer(self, placement):
        return Mengine.appleAppLovinCanOfferRewarded(placement)

    def _canYouShow(self, placement):
        return Mengine.appleAppLovinCanYouShowRewarded(placement)

    def _show(self, placement):
        return Mengine.appleAppLovinShowRewarded(placement)
