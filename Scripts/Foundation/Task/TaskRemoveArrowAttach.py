from Foundation.ArrowManager import ArrowManager
from Foundation.Task.Task import Task

class TaskRemoveArrowAttach(Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskRemoveArrowAttach, self)._onParams(params)
        pass

    def _onRun(self):
        if ArrowManager.emptyArrowAttach() is True:
            return True
            pass

        ArrowManager.removeArrowAttach()

        return True
        pass
    pass