from Foundation.Systems.AppLovin.AndroidAppLovinAdUnit import AndroidAppLovinAdUnit

class AndroidAppLovinInterstitialAd(AndroidAppLovinAdUnit):
    ad_type = "Interstitial"

    def _setCallbacks(self):
        self._addAndroidCallback("onAndroidAdServiceInterstitialShowSuccess", self.cbShowSuccess)
        self._addAndroidCallback("onAndroidAdServiceInterstitialShowFailed", self.cbShowFailed)
        self._addAndroidCallback("onAndroidAdServiceInterstitialRevenuePaid", self.cbRevenuePaid)

    def _cleanUp(self):
        self._removeAndroidCallbacks()

    def _initialize(self):
        self._setCallbacks()
        return True

    def _has(self):
        return Mengine.androidBooleanMethod(self.ANDROID_PLUGIN_NAME, "hasInterstitial")

    def _canYouShow(self, placement):
        return Mengine.androidBooleanMethod(self.ANDROID_PLUGIN_NAME, "canYouShowInterstitial", placement)

    def _show(self, placement):
        return Mengine.androidBooleanMethod(self.ANDROID_PLUGIN_NAME, "showInterstitial", placement)

    def _isShowing(self):
        return Mengine.androidBooleanMethod(self.ANDROID_PLUGIN_NAME, "isInterstitialAdShowing")
