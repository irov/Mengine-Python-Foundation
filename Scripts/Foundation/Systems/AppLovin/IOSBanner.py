from Foundation.Systems.AppLovin.BaseAdUnit import BaseAdUnit, ad_callback


class IOSBanner(BaseAdUnit):
    ad_type = "Banner"

    def _initialize(self):
        callbacks = {
            "onAppleAppLovinBannerRevenuePaid": self.cbRevenuePaid
        }
        return Mengine.appleAppLovinSetBannerProvider(callbacks)

    def _canOffer(self):
        return True

    def _isAvailable(self):
        return True

    def _show(self):
        return Mengine.appleAppLovinShowBanner()

    def hide(self):
        return Mengine.appleAppLovinHideBanner()
