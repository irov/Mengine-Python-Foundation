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

    def __checkAdInterstitial(self, placement):
        if self.isInterstitialEnabled() is False:
            return False

        if placement is None:
            return False

        if AdvertisementProvider.hasInterstitialAdvert() is False:
            return False

        if AdvertisementProvider.canYouShowInterstitialAdvert(placement) is False:
            return False

        return True

    def tryInterstitial(self, next_scene, placement, Skip = False):
        print("SystemAdvertising.tryInterstitial next_scene: ", next_scene, " placement: ", placement, " Skip: ", Skip)

        if self.__checkAdInterstitial(placement) is False:
            if Skip is False:
                Notification.notify(Notificator.onChangeScene, next_scene)
                pass
            return False

        AdvertisingScene = DemonManager.getDemon("AdvertisingScene")
        AdvertisingScene.setParam("NextScene", next_scene)
        AdvertisingScene.setParam("AdPlacement", placement)

        Notification.notify(Notificator.onChangeScene, SystemAdvertising.base_scene_name)

        return True
        pass
