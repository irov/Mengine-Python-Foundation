from Foundation.Systems.AppLovin.BaseAdUnit import BaseAdUnit


class IOSInterstitialAd(BaseAdUnit):
    ad_type = "Interstitial"

    def _initialize(self):
        callbacks = {
            "onAppleAppLovinInterstitialRevenuePaid": self.cbRevenuePaid,
        }
        return Mengine.appleAppLovinSetInterstitialProvider(callbacks)

    def _canOffer(self):
        Trace.log("System", 0, "Interstitial advert works only with isAvailable function")
        return self._isAvailable()

    def _isAvailable(self):
        return Mengine.appleAppLovinCanYouShowInterstitial(self.getPlacementName())

    def _show(self):
        def __showCompleted(successful, params):
            self.cbShowCompleted(successful, params)
            pass

        return Mengine.appleAppLovinShowInterstitial(self.getPlacementName(), __showCompleted)
