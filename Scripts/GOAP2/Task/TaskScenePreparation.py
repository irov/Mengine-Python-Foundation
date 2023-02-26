from GOAP2.SceneManager import SceneManager
from GOAP2.Task.MixinObserver import MixinObserver
from GOAP2.Task.Task import Task

class TaskScenePreparation(MixinObserver, Task):
    Skiped = False

    def _onParams(self, params):
        super(TaskScenePreparation, self)._onParams(params)

        self.SceneName = params.get("SceneName", None)
        pass

    def _onInitialize(self):
        super(TaskScenePreparation, self)._onInitialize()

        if _DEVELOPMENT is True:
            if self.SceneName is None:
                self.initializeFailed("SceneName is None")
                pass

            if SceneManager.hasScene(self.SceneName) is False:
                self.initializeFailed("Scene %s not found" % (self.SceneName))
                pass
            pass
        pass

    def _onCheck(self):
        currentSceneName = SceneManager.getCurrentSceneName()

        if self.SceneName == currentSceneName:
            return False
            pass

        return True
        pass

    def _onRun(self):
        self.addObserver(Notificator.onScenePreparation, self._onSceneFilter)

        return False
        pass

    def _onSceneFilter(self, sceneName):
        if self.SceneName != sceneName:
            return False
            pass

        return True
        pass
    pass