from Foundation.System import System
from Foundation.DefaultManager import DefaultManager
from Foundation.SessionManager import SessionManager
from Foundation.Providers.AdvertisementProvider import AdvertisementProvider

class SystemAutoSave(System):
    def __init__(self):
        super(SystemAutoSave, self).__init__()
        pass

    def _onRun(self):
        if DefaultManager.getDefaultBool("AutoSaveonWillTerminate", False) is True:
            self.addObserver(Notificator.onApplicationWillTerminate, self._willTerminate)

        if DefaultManager.getDefaultBool("AutoSaveWillResignActive", False) is True:
            self.addObserver(Notificator.onApplicationWillResignActive, self._willResignActive)

        if DefaultManager.getDefaultBool("AutoSaveTransition", False) is True:
            self.addObserver(Notificator.onSceneRemoved, self._onSceneRemoved)

        return True

    def _willTerminate(self):
        self.autoSave()

        return False

    def _willResignActive(self):
        if AdvertisementProvider.isShowingInterstitialAdvert() is True:
            return False

        if AdvertisementProvider.isShowingRewardedAdvert() is True:
            return False

        self.autoSave()

        return False

    def _onSceneRemoved(self, SceneName):
        self.autoSave()

        return False

    def autoSave(self):
        Trace.msg("SystemAutoSave auto save session")

        if SessionManager.saveSession() is False:
            Trace.log("System", 0, "SystemAutoSave invalid save session")
        pass