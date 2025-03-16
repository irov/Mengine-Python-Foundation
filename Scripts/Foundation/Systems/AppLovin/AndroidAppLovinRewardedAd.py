from Foundation.Systems.AppLovin.AndroidAppLovinAdUnit import AndroidAppLovinAdUnit

class AndroidAppLovinRewardedAd(AndroidAppLovinAdUnit):
    ad_type = "Rewarded"

    def _setCallbacks(self):
        self._addAndroidCallback("onAndroidAdServiceRewardedShowSuccess", self.cbShowSuccess)
        self._addAndroidCallback("onAndroidAdServiceRewardedShowFailed", self.cbShowFailed)
        self._addAndroidCallback("onAndroidAdServiceRewardedUserRewarded", self.cbUserRewarded)
        self._addAndroidCallback("onAndroidAdServiceRewardedRevenuePaid", self.cbRevenuePaid)

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
        return Mengine.androidBooleanMethod(self.ANDROID_PLUGIN_NAME, "showRewarded", placement)