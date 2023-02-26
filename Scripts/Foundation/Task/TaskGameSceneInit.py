from Foundation.SceneManager import SceneManager
from Foundation.Task.MixinObserver import MixinObserver
from Foundation.Task.Task import Task

class TaskGameSceneInit(MixinObserver, Task):
    Skiped = False

    def _onParams(self, params):
        super(TaskGameSceneInit, self)._onParams(params)
        self.LayerScene = params.get("LayerScene", None)
        pass

    def _onInitialize(self):
        super(TaskGameSceneInit, self)._onInitialize()
        pass

    def _onCheck(self):
        if SceneManager.isChangeScene() is True:
            return True
            pass

        CurrentSceneName = SceneManager.getCurrentSceneName()

        if SceneManager.isGameScene(CurrentSceneName) is False:
            return True
            pass

        return False
        pass

    def _onRun(self):
        self.addObserver(Notificator.onSceneInit, self._onSceneFilter)

        return False
        pass

    def _onSceneFilter(self, sceneName):
        if SceneManager.isGameScene(sceneName) is False:
            return False
            pass

        if self.LayerScene is not None:
            hasLayerScene = SceneManager.hasLayerScene(self.LayerScene)

            if hasLayerScene is False:
                return False
                pass
            pass

        return True
        pass
    pass