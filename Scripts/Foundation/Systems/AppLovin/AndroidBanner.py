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

    def _canOffer(self):
        Trace.log("System", 0, "Banner function 'canOffer' always returns True")
        return True

    def _isAvailable(self):
        Trace.log("System", 0, "Banner function 'isAvailable' always returns True")
        return True

    def _show(self):
        return Mengine.androidBooleanMethod(self.ANDROID_PLUGIN_NAME, "bannerVisible", True)

    def hide(self):
        return Mengine.androidBooleanMethod(self.ANDROID_PLUGIN_NAME, "bannerVisible", False)

    # callbacks

    @ad_callback
    def cbExpanded(self):
        self._cbExpanded()

    def _cbExpanded(self):
        self._log("[{} cb] {} was expanded".format(self.ad_type, self.name))

    @ad_callback
    def cbCollapsed(self):
        self._cbCollapsed()

    def _cbCollapsed(self):
        self._log("[{} cb] {} was collapsed".format(self.ad_type, self.name))
