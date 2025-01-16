from Foundation.Systems.AppLovin.BaseAdUnit import BaseAdUnit, AndroidAdUnitCallbacks

class AndroidInterstitialAd(BaseAdUnit, AndroidAdUnitCallbacks):
    ad_type = "Interstitial"

    def _setCallbacks(self):
        self._addAndroidCallback("onAppLovinInterstitialRevenuePaid", self.cbRevenuePaid)

    def _cleanUp(self):
        self._removeAndroidCallbacks()

    def _initialize(self):
        self._setCallbacks()
        return True

    def _canOffer(self):
        Trace.log("System", 0, "Interstitial advert works only with isAvailable function")
        return self._isAvailable()

    def _isAvailable(self):
        return Mengine.androidBooleanMethod(self.ANDROID_PLUGIN_NAME, "canYouShowInterstitial", self.getPlacementName())

    def _show(self, cb):
        return Mengine.androidBooleanMethod(self.ANDROID_PLUGIN_NAME, "showInterstitial", self.getPlacementName(), cb)
