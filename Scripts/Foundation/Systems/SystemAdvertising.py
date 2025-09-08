from Foundation.System import System

from Foundation.Providers.AdvertisementProvider import AdvertisementProvider
from Foundation.DefaultManager import DefaultManager
from Foundation.PolicyManager import PolicyManager
from Foundation.DemonManager import DemonManager
from Foundation.TaskManager import TaskManager

class SystemAdvertising(System):
    ADVERTISING_SCENE = "Advertising"
    IGNORE_SCENES = ["CutScene", "Dialog"]

    def __init__(self):
        super(SystemAdvertising, self).__init__()
        pass

    def _onInitialize(self):
        PolicyAliasTransitionAdvertising = DefaultManager.getDefault("AliasTransition", default="PolicyAliasTransitionAdvertising")

        PolicyManager.setPolicy("AliasTransition", PolicyAliasTransitionAdvertising)
        pass

    def isInterstitialEnabled(self):
        if Mengine.getConfigBool("Advertising", "Interstitial", False) is False:
            return False

        if Mengine.hasTouchpad() is False:
            if _DEVELOPMENT is True:
                Trace.msg("Advertising works only with touchpad! (add -touchpad)")
            return False

        return True

    def tryInterstitial(self, next_scene, placement, Skip = False):
        def __checkAdInterstitial(placement):
            if self.isInterstitialEnabled() is False:
                return False

            if placement is None:
                return False

            if AdvertisementProvider.hasInterstitialAdvert() is False:
                return False

            if AdvertisementProvider.canYouShowInterstitialAdvert(placement) is False:
                return False

            return True

        if __checkAdInterstitial(placement) is False:
            if Skip is False:
                Notification.notify(Notificator.onChangeScene, next_scene)
                pass
            return False

        AdvertisingScene = DemonManager.getDemon("AdvertisingScene")
        AdvertisingScene.setParam("NextScene", next_scene)
        AdvertisingScene.setParam("AdPlacement", placement)

        Notification.notify(Notificator.onChangeScene, SystemAdvertising.ADVERTISING_SCENE)

        return True
