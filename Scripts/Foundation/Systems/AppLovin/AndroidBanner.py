from Foundation.Systems.AppLovin.BaseAdUnit import BaseAdUnit, AndroidAdUnitCallbacks
from Foundation.Systems.AppLovin.BaseAdUnit import ad_callback

class AndroidBanner(BaseAdUnit, AndroidAdUnitCallbacks):
    ad_type = "Banner"

    def _setCallbacks(self):
        self._addAndroidCallback("onAndroidAppLovinBannerRevenuePaid", self.cbRevenuePaid)

    def _cleanUp(self):
        self._removeAndroidCallbacks()

    def _initialize(self):
        self._setCallbacks()
        return True

    def _has(self):
        return Mengine.androidMethod(self.ANDROID_PLUGIN_NAME, "hasBanner")

    def _canOffer(self, placement):
        return True

    def _canYouShow(self, placement):
        return True

    def _show(self, placement):
        return Mengine.androidMethod(self.ANDROID_PLUGIN_NAME, "showBanner")

    def _hide(self, placement):
        return Mengine.androidMethod(self.ANDROID_PLUGIN_NAME, "hideBanner")
