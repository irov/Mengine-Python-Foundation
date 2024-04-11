from Foundation.Systems.AppLovin.BaseAdUnit import BaseAdUnit, AndroidAdUnitCallbacks
from Foundation.Systems.AppLovin.BaseAdUnit import ad_callback


class AndroidBanner(BaseAdUnit, AndroidAdUnitCallbacks):
    ad_type = "Banner"

    def _setCallbacks(self):
        self._addAndroidCallback("onAppLovinBannerOnAdDisplayed", self.cbDisplaySuccess)
        self._addAndroidCallback("onAppLovinBannerOnAdDisplayFailed", self.cbDisplayFailed)
        self._addAndroidCallback("onAppLovinBannerOnAdClicked", self.cbClicked)
        self._addAndroidCallback("onAppLovinBannerOnAdHidden", self.cbHidden)
        self._addAndroidCallback("onAppLovinBannerOnAdExpanded", self.cbExpanded)
        self._addAndroidCallback("onAppLovinBannerOnAdCollapsed", self.cbCollapsed)
        self._addAndroidCallback("onAppLovinBannerOnAdLoaded", self.cbLoadSuccess)
        self._addAndroidCallback("onAppLovinBannerOnAdLoadFailed", self.cbLoadFailed)
        self._addAndroidCallback("onAppLovinBannerOnAdRevenuePaid", self.cbPayRevenue)

    def _cleanUp(self):
        self._removeAndroidCallbacks()

    def _initialize(self):
        self._setCallbacks()
        return Mengine.androidBooleanMethod(self.ANDROID_PLUGIN_NAME, "initBanner",
                                            self.ad_unit_id, self.getPlacementName())

    def _canOffer(self):
        Trace.log("System", 0, "Banner function 'canOffer' always returns True")
        return True

    def _isAvailable(self):
        Trace.log("System", 0, "Banner function 'isAvailable' always returns True")
        return True

    def _show(self):
        return Mengine.androidBooleanMethod(self.ANDROID_PLUGIN_NAME, "bannerVisible",
                                            self.ad_unit_id, True)

    def hide(self):
        return Mengine.androidBooleanMethod(self.ANDROID_PLUGIN_NAME, "bannerVisible",
                                            self.ad_unit_id, False)

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
