from Foundation.Systems.AppLovin.BaseAdUnit import BaseAdUnit
from Foundation.Systems.AppLovin.BaseAdUnit import ad_callback


class IOSRewardedAd(BaseAdUnit):
    ad_type = "Rewarded"

    def _initialize(self):
        callbacks = {
            "onAppleAppLovinRewardedDidDisplayAd": self.cbDisplaySuccess,
            "onAppleAppLovinRewardedDidFailToDisplayAd": self.cbDisplayFailed,
            "onAppleAppLovinRewardedDidClickAd": self.cbClicked,
            "onAppleAppLovinRewardedDidHideAd": self.cbHidden,
            "onAppleAppLovinRewardedDidRewardUserForAd": self.cbUserRewarded,
            "onAppleAppLovinRewardedDidLoadAd": self.cbLoadSuccess,
            "onAppleAppLovinRewardedDidFailToLoadAdForAdUnitIdentifier": self.cbLoadFailed,
            "onAppleAppLovinRewardedDidPayRevenueForAd": self.cbPayRevenue,
        }
        return Mengine.appleAppLovinInitRewarded(callbacks)

    def _canOffer(self):
        return Mengine.appleAppLovinCanOfferRewarded(self.getPlacementName())

    def _isAvailable(self):
        return Mengine.appleAppLovinCanYouShowRewarded(self.getPlacementName())

    def _show(self):
        return Mengine.appleAppLovinShowRewarded(self.getPlacementName())

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
