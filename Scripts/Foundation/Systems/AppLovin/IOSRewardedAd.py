from Foundation.Systems.AppLovin.BaseAdUnit import BaseAdUnit
from Foundation.Systems.AppLovin.BaseAdUnit import ad_callback


class IOSRewardedAd(BaseAdUnit):
    ad_type = "Rewarded"

    def _initialize(self):
        callbacks = {
            "onAppleAppLovinRewardedUserRewarded": self.cbUserRewarded,
            "onAndroidAppLovinRewardedRevenuePaid": self.cbRevenuePaid,
        }
        return Mengine.appleAppLovinSetRewardedProvider(callbacks)

    def _canOffer(self):
        return Mengine.appleAppLovinCanOfferRewarded(self.getPlacementName())

    def _isAvailable(self):
        return Mengine.appleAppLovinCanYouShowRewarded(self.getPlacementName())

    def _show(self):
        def __showCompleted(successful, params):
            self.cbShowCompleted(successful, params)
            pass

        return Mengine.appleAppLovinShowRewarded(self.getPlacementName(), __showCompleted)

    # callbacks

    @ad_callback
    def cbUserRewarded(self, params):
        self._cbUserRewarded(params)

    def _cbUserRewarded(self, params):
        self._log("[{} cb] user rewarded: {}".format(self.name, params))
        Notification.notify(Notificator.onAdUserRewarded, self.ad_type, self.name, params)
