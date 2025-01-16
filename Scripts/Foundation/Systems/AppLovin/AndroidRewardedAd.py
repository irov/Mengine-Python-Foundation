from Foundation.Systems.AppLovin.BaseAdUnit import BaseAdUnit, AndroidAdUnitCallbacks
from Foundation.Systems.AppLovin.BaseAdUnit import ad_callback

class AndroidRewardedAd(BaseAdUnit, AndroidAdUnitCallbacks):
    ad_type = "Rewarded"

    def _setCallbacks(self):
        self._addAndroidCallback("onAndroidAppLovinRewardedUserRewarded", self.cbUserRewarded)
        self._addAndroidCallback("onAndroidAppLovinRewardedRevenuePaid", self.cbRevenuePaid)

    def _cleanUp(self):
        self._removeAndroidCallbacks()

    def _initialize(self):
        self._setCallbacks()
        return True

    def _canOffer(self):
        return Mengine.androidBooleanMethod(self.ANDROID_PLUGIN_NAME, "canOfferRewarded", self.getPlacementName())

    def _isAvailable(self):
        return Mengine.androidBooleanMethod(self.ANDROID_PLUGIN_NAME, "canYouShowRewarded", self.getPlacementName())

    def _show(self, cb):
        return Mengine.androidBooleanMethod(self.ANDROID_PLUGIN_NAME, "showRewarded", self.getPlacementName(), cb)

    # callbacks

    @ad_callback
    def cbUserRewarded(self, params):
        self._cbUserRewarded(params)

    def _cbUserRewarded(self, params):
        self._log("[{} cb] user rewarded: {}".format(self.name, params))
        Notification.notify(Notificator.onAdUserRewarded, self.ad_type, self.name, params)