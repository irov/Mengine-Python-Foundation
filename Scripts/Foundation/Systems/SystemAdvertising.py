from Foundation.System import System

from Foundation.DefaultManager import DefaultManager
from Foundation.Providers.AdvertisementProvider import AdvertisementProvider
from Foundation.TaskManager import TaskManager

class SystemAdvertising(System):
    def isInterstitialEnabled(self):
        if Mengine.getConfigBool("Advertising", "Interstitial", False) is False:
            return False

        if Mengine.hasTouchpad() is False:
            if _DEVELOPMENT is True:
                Trace.msg("Advertising works only with touchpad! (add -touchpad)")
            return False

        return True

    def tryInterstitial(self, next_scene, placement, Skip = False):
        if AdvertisementProvider.s_fullscreen_ad_showing is True:
            if Skip is False:
                with TaskManager.createTaskChain(Global=True) as tc:
                    with tc.addRaceTask(2) as (completed, timeout):
                        completed.addListener(Notificator.onAdShowCompleted)
                        timeout.addDelay(DefaultManager.getDefaultInt("FullscreenAdvertShowTimeout", 60) * 1000.0)
                        timeout.addFunction(AdvertisementProvider.resetFullscreenAdvertState)

                    tc.addNotify(Notificator.onChangeScene, next_scene)

            return True

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
            return False

        task_chain = TaskManager.createTaskChain(CallerDeep=1, Global=True)

        if task_chain is None:
            if Skip is False:
                Notification.notify(Notificator.onChangeScene, next_scene)
            return False

        with task_chain as source:
            source.addTask(
                "AliasShowInterstitialAdvert",
                AdPlacement=placement
            )

            source.addNotify(Notificator.onChangeScene, next_scene)

        return True
