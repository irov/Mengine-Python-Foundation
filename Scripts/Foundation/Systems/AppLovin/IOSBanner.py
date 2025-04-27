from Foundation.Systems.AppLovin.BaseAdUnit import BaseAdUnit

class IOSBanner(BaseAdUnit):
    ad_type = "Banner"

    def _initialize(self):
        callbacks = {
            "onAppleAdvertisementRevenuePaid": self.cbRevenuePaid
        }

        return Mengine.appleAdvertisementSetBannerCallback(callbacks)

    def _has(self):
        return Mengine.appleAdvertisementHasBanner()

    def _canOffer(self):
        return True

    def _canYouShow(self):
        return True

    def _show(self, placement):
        return Mengine.appleAdvertisementShowBanner()

    def _hide(self, placement):
        return Mengine.appleAdvertisementHideBanner()
