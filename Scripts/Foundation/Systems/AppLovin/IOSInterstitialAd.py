from Foundation.Systems.AppLovin.BaseAdUnit import BaseAdUnit


class IOSInterstitialAd(BaseAdUnit):
    ad_type = "Interstitial"

    def _initialize(self):
        callbacks = {
            "onAppleAppLovinInterstitialShowSuccessful": self.cbShowSuccessful,
            "onAppleAppLovinInterstitialShowFailed": self.cbShowFailed,
            "onAppleAppLovinInterstitialRevenuePaid": self.cbRevenuePaid
        }
        return Mengine.appleAppLovinSetInterstitialProvider(callbacks)

    def _has(self):
        return Mengine.appleAppLovinHasInterstitial()

    def _canYouShow(self, placement):
        return Mengine.appleAppLovinCanYouShowInterstitial(placement)

    def _show(self, placement):
        return Mengine.appleAppLovinShowInterstitial(placement)
