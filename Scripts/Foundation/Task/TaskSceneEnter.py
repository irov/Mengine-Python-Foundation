from Foundation.SceneManager import SceneManager
from Foundation.Task.MixinObserver import MixinObserver
from Foundation.Task.Task import Task

class TaskSceneEnter(MixinObserver, Task):
    Skiped = False

    def _onParams(self, params):
        super(TaskSceneEnter, self)._onParams(params)

        self.SceneName = params.get("SceneName", None)
        self.SceneAny = params.get("SceneAny", False)
        self.isEnter = params.get("isEnter", True)
        pass

    def _onInitialize(self):
        super(TaskSceneEnter, self)._onInitialize()

        if _DEVELOPMENT is True:
            if self.SceneAny is False:
                if self.SceneName is None:
                    self.initializeFailed("SceneName is None")
                    pass

                if SceneManager.hasScene(self.SceneName) is False:
                    self.initializeFailed("Scene %s not found" % (self.SceneName))
                    pass
                pass
            pass
        pass

    def _onCheck(self):
        if self.isEnter is False:
            return True
            pass

        if self.SceneAny is False:
            if SceneManager.isSceneEnter(self.SceneName) is True:
                return False
                pass
            pass
        else:
            if SceneManager.isCurrentSceneEntering() is True:
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
        if self.SceneAny is True:
            return True
            pass

        if self.SceneName != SceneName:
            return False
            pass

        return True
        pass
    pass