from Foundation.SceneManager import SceneManager
from Foundation.Task.Task import Task

class TaskGameScenesBlock(Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskGameScenesBlock, self)._onParams(params)
        self.Value = params.get("Value")
        pass

    def _onInitialize(self):
        super(TaskGameScenesBlock, self)._onInitialize()
        pass

    def _onRun(self):
        SceneManager.blockGameScenes(self.Value)
        return True
        pass
    pass