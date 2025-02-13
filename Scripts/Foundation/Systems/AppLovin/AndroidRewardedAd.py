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

    def _has(self):
        return Mengine.androidBooleanMethod(self.ANDROID_PLUGIN_NAME, "hasRewarded")

    def _canOffer(self, placement):
        return Mengine.androidBooleanMethod(self.ANDROID_PLUGIN_NAME, "canOfferRewarded", placement)

    def _canYouShow(self, placement):
        return Mengine.androidBooleanMethod(self.ANDROID_PLUGIN_NAME, "canYouShowRewarded", placement)

    def _show(self, placement):
        def __showCompleted(successful, params):
            self.cbShowCompleted(successful, params)
            pass

        return Mengine.androidBooleanMethod(self.ANDROID_PLUGIN_NAME, "showRewarded", placement, __showCompleted)

    # callbacks

    @ad_callback
    def cbUserRewarded(self, params):
        self._cbUserRewarded(params)

    def _cbUserRewarded(self, params):
        self._log("[{} cb] user rewarded: {}".format(self.name, params))
        Notification.notify(Notificator.onAdUserRewarded, self.ad_type, self.name, params)