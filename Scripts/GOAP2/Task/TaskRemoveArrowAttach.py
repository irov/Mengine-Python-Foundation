from GOAP2.ArrowManager import ArrowManager
from GOAP2.Task.Task import Task

class TaskRemoveArrowAttach(Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskRemoveArrowAttach, self)._onParams(params)
        pass

    def _onRun(self):
        if ArrowManager.emptyArrowAttach() is True:
            ArrowManager.removeChildren()
            return True
            pass

        ArrowManager.removeArrowAttach()

        return True
        pass
    pass