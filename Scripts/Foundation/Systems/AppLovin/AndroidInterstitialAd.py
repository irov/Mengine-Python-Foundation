from Foundation.Systems.AppLovin.BaseAdUnit import BaseAdUnit, AndroidAdUnitCallbacks


class AndroidInterstitialAd(BaseAdUnit, AndroidAdUnitCallbacks):
    ad_type = "Interstitial"

    def _setCallbacks(self):
        self._addAndroidCallback("onAppLovinInterstitialOnAdDisplayed", self.cbDisplaySuccess)
        self._addAndroidCallback("onAppLovinInterstitialOnAdDisplayFailed", self.cbDisplayFailed)
        self._addAndroidCallback("onAppLovinInterstitialOnAdClicked", self.cbClicked)
        self._addAndroidCallback("onAppLovinInterstitialOnAdHidden", self.cbHidden)
        self._addAndroidCallback("onAppLovinInterstitialOnAdLoaded", self.cbLoadSuccess)
        self._addAndroidCallback("onAppLovinInterstitialOnAdLoadFailed", self.cbLoadFailed)
        self._addAndroidCallback("onAppLovinInterstitialOnAdRevenuePaid", self.cbPayRevenue)

    def _cleanUp(self):
        self._removeAndroidCallbacks()

    def _initialize(self):
        self._setCallbacks()
        return Mengine.androidBooleanMethod(self.ANDROID_PLUGIN_NAME, "initInterstitial",
                                            self.ad_unit_id)

    def _canOffer(self):
        Trace.log("System", 0, "Interstitial advert works only with isAvailable function")
        return self._isAvailable()

    def _isAvailable(self):
        return Mengine.androidBooleanMethod(self.ANDROID_PLUGIN_NAME, "canYouShowInterstitial",
                                            self.ad_unit_id, self.getPlacementName())

    def _show(self):
        return Mengine.androidBooleanMethod(self.ANDROID_PLUGIN_NAME, "showInterstitial",
                                            self.ad_unit_id, self.getPlacementName())
