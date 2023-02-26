from Foundation.ArrowManager import ArrowManager
from Foundation.Task.Task import Task

class TaskArrowModeChange(Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskArrowModeChange, self)._onParams(params)
        self.ModeName = params.get("ModeName", "Default")
        pass

    def _onCheck(self):
        currentMode = ArrowManager.getArrowCursor()
        if currentMode == self.ModeName:
            return False
            pass
        return True
        pass

    def _onRun(self):
        ArrowManager.setArrowCursor(self.ModeName)

        return True
        pass
    pass