from Foundation.Systems.AppLovin.BaseAdUnit import BaseAdUnit


class IOSInterstitialAd(BaseAdUnit):
    ad_type = "Interstitial"

    def _initialize(self):
        callbacks = {
            "onAppleAppLovinInterstitialRevenuePaid": self.cbRevenuePaid,
        }
        return Mengine.appleAppLovinSetInterstitialProvider(callbacks)

    def _has(self, placement):
        return Mengine.appleAppLovinHasInterstitial(placement)

    def _canYouShow(self, placement):
        return Mengine.appleAppLovinCanYouShowInterstitial(placement)

    def _show(self, placement):
        def __showCompleted(successful, params):
            self.cbShowCompleted(successful, params)
            pass

        return Mengine.appleAppLovinShowInterstitial(placement, __showCompleted)
