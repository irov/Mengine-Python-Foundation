from Foundation.GameManager import GameManager
from Foundation.Task.Task import Task

class TaskGameBlock(Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskGameBlock, self)._onParams(params)

        self.Value = params.get("Value")
        pass

    def _onRun(self):
        GameManager.blockGame(self.Value)

        return True
        pass
    pass