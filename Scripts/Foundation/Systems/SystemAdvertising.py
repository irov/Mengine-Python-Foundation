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
        AdvertisingTransitionPolicyName = DefaultManager.getDefault("AdvertisingTransitionPolicyName", default="PolicyTransitionAdvertising")

        PolicyManager.setPolicy("Transition", AdvertisingTransitionPolicyName)
        pass

    def isInterstitialEnabled(self):
        if Mengine.getConfigBool("Advertising", "Interstitial", False) is False:
            return False

        if Mengine.hasTouchpad() is False:
            if _DEVELOPMENT is True:
                Trace.msg("Advertising works only with touchpad! (add -touchpad)")
            return False

        return True

    def __checkAdInterstitial(self, TransitionData, Placement):
        if TransitionData.get("SceneName") in SystemAdvertising.IGNORE_SCENES:
            return False

        if self.isInterstitialEnabled() is False:
            return False

        if Placement is None:
            return False

        if AdvertisementProvider.hasInterstitialAdvert() is False:
            return False

        if AdvertisementProvider.canYouShowInterstitialAdvert(Placement) is False:
            return False

        return True

    def tryInterstitial(self, next_scene, placement, Skip = False):
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
