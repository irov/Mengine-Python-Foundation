from Foundation.Systems.AppLovin.BaseAdUnit import BaseAdUnit

class IOSBanner(BaseAdUnit):
    ad_type = "Banner"

    def _initialize(self):
        callbacks = {
            "onAppleAppLovinBannerRevenuePaid": self.cbRevenuePaid
        }
        return Mengine.appleAppLovinSetBannerProvider(callbacks)

    def _has(self):
        return Mengine.appleAppLovinHasBanner()

    def _canOffer(self):
        return True

    def _canYouShow(self):
        return True

    def _show(self, placement):
        return Mengine.appleAppLovinShowBanner()

    def _hide(self, placement):
        return Mengine.appleAppLovinHideBanner()
