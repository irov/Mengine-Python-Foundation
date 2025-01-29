from Foundation.Systems.AppLovin.BaseAdUnit import BaseAdUnit, AndroidAdUnitCallbacks

class AndroidInterstitialAd(BaseAdUnit, AndroidAdUnitCallbacks):
    ad_type = "Interstitial"

    def _setCallbacks(self):
        self._addAndroidCallback("onAndroidAppLovinInterstitialRevenuePaid", self.cbRevenuePaid)

    def _cleanUp(self):
        self._removeAndroidCallbacks()

    def _initialize(self):
        self._setCallbacks()
        return True

    def _has(self, placement):
        return Mengine.androidBooleanMethod(self.ANDROID_PLUGIN_NAME, "hasInterstitial", placement)

    def _canYouShow(self, placement):
        return Mengine.androidBooleanMethod(self.ANDROID_PLUGIN_NAME, "canYouShowInterstitial", placement)

    def _show(self, placement):
        def __showCompleted(successful, params):
            self.cbShowCompleted(successful, params)
            pass

        return Mengine.androidBooleanMethod(self.ANDROID_PLUGIN_NAME, "showInterstitial", placement, __showCompleted)
