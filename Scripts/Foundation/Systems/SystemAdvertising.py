from Foundation.System import System

from Foundation.Providers.AdvertisementProvider import AdvertisementProvider
from Foundation.DemonManager import DemonManager

class SystemAdvertising(System):
    base_scene_name = "Advertising"

    def __init__(self):
        super(SystemAdvertising, self).__init__()
        pass

    def isInterstitialEnabled(self):
        if Mengine.getConfigBool("Advertising", "Interstitial", False) is False:
            return False
        if Mengine.hasTouchpad() is False:
            if _DEVELOPMENT is True:
                Trace.msg_err("Advertising works only with touchpad! (add -touchpad)")
            return False

        return True

    def __checkAdInterstitial(self, AdPlacement):
        """ checks if interstitial is allowed and ad point exists, enabled """
        if self.isInterstitialEnabled() is False:
            return False

        if AdPlacement is None:
            Trace.log("Object", 0, "AdPlacement not setup")
            return False

        if AdvertisementProvider.hasInterstitialAdvert() is False:
            Trace.log("Object", 0, "AdPoint {!r} has interstitial advert is False".format(AdPlacement))
            return False

        if AdvertisementProvider.canYouShowInterstitialAdvert(AdPlacement) is False:
            Trace.log("Object", 0, "AdPoint {!r} can you show is False".format(AdPlacement))
            return False

        return True

    def tryInterstitial(self, next_scene, AdPlacement, Skip = False):
        if self.__checkAdInterstitial(AdPlacement) is False:
            if Skip is True:
                Notification.notify(Notificator.onChangeScene, next_scene)
                pass
            return

        AdvertisingScene = DemonManager.getDemon("AdvertisingScene")
        AdvertisingScene.setParam("NextScene", next_scene)
        AdvertisingScene.setParam("AdPlacement", AdPlacement)

        Notification.notify(Notificator.onChangeScene, SystemAdvertising.base_scene_name)
        pass
