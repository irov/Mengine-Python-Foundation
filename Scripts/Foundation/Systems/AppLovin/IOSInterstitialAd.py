from Foundation.Systems.AppLovin.BaseAdUnit import BaseAdUnit


class IOSInterstitialAd(BaseAdUnit):

    def _initialize(self):
        callbacks = {
            "onAppLovinInterstitialOnAdDisplayed": self.cbDisplaySuccess,
            "onAppLovinInterstitialOnAdDisplayFailed": self.cbDisplayFailed,
            "onAppLovinInterstitialOnAdClicked": self.cbClicked,
            "onAppLovinInterstitialOnAdHidden": self.cbHidden,
            "onAppLovinInterstitialOnAdLoaded": self.cbLoadSuccess,
            "onAppLovinInterstitialOnAdLoadFailed": self.cbLoadFailed,
            "onAppLovinInterstitialOnAdRevenuePaid": self.cbPayRevenue,
        }
        return Mengine.appleAppLovinInitInterstitial(self.ad_unit_id, callbacks)

    def _canOffer(self):
        Trace.log("System", 0, "Interstitial advert works only with isAvailable function")
        return self._isAvailable()

    def _isAvailable(self):
        return Mengine.appleAppLovinCanYouShowInterstitial(self.ad_unit_id, self.getPlacementName())

    def _show(self):
        return Mengine.appleAppLovinShowInterstitial(self.ad_unit_id, self.getPlacementName())
