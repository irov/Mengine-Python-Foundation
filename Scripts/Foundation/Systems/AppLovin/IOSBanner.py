from Foundation.Systems.AppLovin.BaseAdUnit import BaseAdUnit, ad_callback


class IOSBanner(BaseAdUnit):
    ad_type = "Banner"

    def _initialize(self):
        callbacks = {
            "onAppleAppLovinInterstitialDidDisplayAd": self.cbDisplaySuccess,
            "onAppleAppLovinBannerDidFailToDisplayAd": self.cbDisplayFailed,
            "onAppleAppLovinBannerDidClickAd": self.cbClicked,
            # "null": self.cbHidden,
            "onAppleAppLovinBannerDidExpandAd": self.cbExpanded,
            "onAppleAppLovinBannerDidCollapseAd": self.cbCollapsed,
            "onAppleAppLovinBannerDidLoadAd": self.cbLoadSuccess,
            "onAppleAppLovinBannerDidFailToLoadAdForAdUnitIdentifier": self.cbLoadFailed,
            "onAppleAppLovinBannerDidPayRevenueForAd": self.cbPayRevenue,
            # onAppleAppLovinBannerDidStartAdRequestForAdUnitIdentifier
        }
        return Mengine.appleAppLovinInitBanner(self.ad_unit_id, self.getPlacementName(), callbacks)

    def _canOffer(self):
        return True

    def _isAvailable(self):
        return True

    def _show(self):
        return Mengine.appleAppLovinShowBanner(self.ad_unit_id)

    def hide(self):
        return Mengine.appleAppLovinHideBanner(self.ad_unit_id)

    # callbacks

    @ad_callback
    def cbExpanded(self):
        self._cbExpanded()

    def _cbExpanded(self):
        self._log("[{} cb] {} was expanded".format(self.ad_type, self.name))

    @ad_callback
    def cbCollapsed(self):
        self._cbCollapsed()

    def _cbCollapsed(self):
        self._log("[{} cb] {} was collapsed".format(self.ad_type, self.name))
