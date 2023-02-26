from GOAP2.SceneManager import SceneManager
from GOAP2.Task.MixinObserver import MixinObserver
from GOAP2.Task.Task import Task

class TaskSceneLeave(MixinObserver, Task):
    Skiped = False

    def _onParams(self, params):
        super(TaskSceneLeave, self)._onParams(params)

        self.SceneName = params.get("SceneName", None)
        self.SceneAny = params.get("SceneAny", False)
        pass

    def _onInitialize(self):
        super(TaskSceneLeave, self)._onInitialize()

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
        if self.SceneAny is False:
            if SceneManager.isSceneEnter(self.SceneName) is True:
                return True
                pass
            pass
        else:
            if SceneManager.isCurrentSceneEntering() is False:
                return False
                pass
            pass

        return True
        pass

    def _onRun(self):
        self.addObserver(Notificator.onSceneLeave, self._onSceneLeaveFilter)

        return False
        pass

    def _onSceneLeaveFilter(self, SceneName):
        if self.SceneAny is True:
            return True
            pass

        if self.SceneName != SceneName:
            return False
            pass

        return True
        pass
    pass