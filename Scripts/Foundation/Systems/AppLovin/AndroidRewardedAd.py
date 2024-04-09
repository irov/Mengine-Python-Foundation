from Foundation.Systems.AppLovin.BaseAdUnit import BaseAdUnit, AndroidAdUnitCallbacks
from Foundation.Systems.AppLovin.BaseAdUnit import ad_callback


class AndroidRewardedAd(BaseAdUnit, AndroidAdUnitCallbacks):

    def _setCallbacks(self):
        self._addAndroidCallback("onAppLovinRewardedOnAdDisplayed", self.cbDisplaySuccess)
        self._addAndroidCallback("onAppLovinRewardedOnAdDisplayFailed", self.cbDisplayFailed)
        self._addAndroidCallback("onAppLovinRewardedOnAdClicked", self.cbClicked)
        self._addAndroidCallback("onAppLovinRewardedOnAdHidden", self.cbHidden)
        self._addAndroidCallback("onAppLovinRewardedOnUserRewarded", self.cbUserRewarded)
        self._addAndroidCallback("onAppLovinRewardedOnAdLoaded", self.cbLoadSuccess)
        self._addAndroidCallback("onAppLovinRewardedOnAdLoadFailed", self.cbLoadFailed)
        self._addAndroidCallback("onAppLovinRewardedOnAdRevenuePaid", self.cbPayRevenue)

    def _cleanUp(self):
        self._removeAndroidCallbacks()

    def _initialize(self):
        self._setCallbacks()
        return Mengine.androidBooleanMethod(self.ANDROID_PLUGIN_NAME, "initRewarded",
                                            self.ad_unit_id)

    def _canOffer(self):
        return Mengine.androidBooleanMethod(self.ANDROID_PLUGIN_NAME, "canOfferRewarded",
                                            self.ad_unit_id, self.getPlacementName())

    def _isAvailable(self):
        return Mengine.androidBooleanMethod(self.ANDROID_PLUGIN_NAME, "canYouShowRewarded",
                                            self.ad_unit_id, self.getPlacementName())

    def _show(self):
        return Mengine.androidBooleanMethod(self.ANDROID_PLUGIN_NAME, "showRewarded",
                                            self.ad_unit_id, self.getPlacementName())

    # callbacks

    @ad_callback
    def cbUserRewarded(self, label="", reward=1):
        self._cbUserRewarded(label, reward)

    def _cbUserRewarded(self, label, reward):
        self.rewarded = True
        Notification.notify(Notificator.onAdvertRewarded, self.name, label, reward)
        self._log("[{} cb] user rewarded: label={!r}, amount={!r}".format(self.name, label, reward))

    def _cbDisplaySuccess(self):
        self.rewarded = False
        super(self.__class__, self)._cbDisplaySuccess()

    def _cbHidden(self):
        if self.rewarded is False:
            Notification.notify(Notificator.onAdvertSkipped, self.ad_type, self.name)
            self._log("[{} cb] advert {!r} was skipped".format(self.ad_type, self.name))
        super(self.__class__, self)._cbHidden()
