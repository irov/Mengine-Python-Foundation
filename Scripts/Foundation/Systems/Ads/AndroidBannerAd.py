from Foundation.Systems.Ads.AndroidAdUnit import AndroidAdUnit

class AndroidBannerAd(AndroidAdUnit):
    ad_type = "Banner"

    def _setCallbacks(self):
        self._addAndroidCallback("onAndroidAdServiceBannerRevenuePaid", self.cbRevenuePaid)

    def _cleanUp(self):
        self._removeAndroidCallbacks()

    def _initialize(self):
        self._setCallbacks()
        return True

    def _has(self):
        return Mengine.androidBooleanMethod(self.ANDROID_PLUGIN_NAME, "hasBanner")

    def _canOffer(self, placement):
        return True

    def _canYouShow(self, placement):
        return True

    def _show(self, placement):
        return Mengine.androidMethod(self.ANDROID_PLUGIN_NAME, "showBanner")

    def _hide(self, placement):
        return Mengine.androidMethod(self.ANDROID_PLUGIN_NAME, "hideBanner")
