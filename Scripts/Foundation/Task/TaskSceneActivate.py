from Foundation.SceneManager import SceneManager
from Foundation.Task.MixinObserver import MixinObserver
from Foundation.Task.Task import Task

class TaskSceneActivate(MixinObserver, Task):
    Skiped = False

    def _onCheck(self):
        currentSceneName = SceneManager.getCurrentSceneName()

        if currentSceneName is not None:
            if SceneManager.isCurrentSceneActive() is True:
                return False
                pass
            pass

        return True
        pass

    def _onRun(self):
        self.addObserver(Notificator.onSceneInit, self.__onSceneInit)

        return False
        pass

    def __onSceneInit(self, sceneName):
        return True
        pass

    pass