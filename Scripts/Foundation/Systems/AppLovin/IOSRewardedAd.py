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

    def _has(self, placement):
        return Mengine.appleAppLovinHasRewarded(placement)

    def _canOffer(self, placement):
        return Mengine.appleAppLovinCanOfferRewarded(placement)

    def _canYouShow(self, placement):
        return Mengine.appleAppLovinCanYouShowRewarded(placement)

    def _show(self, placement):
        def __showCompleted(successful, params):
            self.cbShowCompleted(successful, params)
            pass

        return Mengine.appleAppLovinShowRewarded(placement, __showCompleted)

    # callbacks

    @ad_callback
    def cbUserRewarded(self, params):
        self._cbUserRewarded(params)

    def _cbUserRewarded(self, params):
        self._log("[{} cb] user rewarded: {}".format(self.name, params))
        Notification.notify(Notificator.onAdUserRewarded, self.ad_type, self.name, params)
