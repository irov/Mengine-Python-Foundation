from Foundation.SceneManager import SceneManager
from Foundation.Task.MixinObserver import MixinObserver
from Foundation.Task.Task import Task

class TaskGameSceneEnter(MixinObserver, Task):
    Skiped = False

    def _onCheck(self):
        if SceneManager.isCurrentSceneEntering() is True:
            if SceneManager.isCurrentGameScene() is True:
                return False
                pass
            pass

        return True
        pass

    def _onRun(self):
        self.addObserver(Notificator.onSceneEnter, self._onSceneEnterFilter)

        return False
        pass

    def _onSceneEnterFilter(self, SceneName):
        if SceneManager.isCurrentGameScene() is False:
            return False
            pass

        return True
        pass
    pass