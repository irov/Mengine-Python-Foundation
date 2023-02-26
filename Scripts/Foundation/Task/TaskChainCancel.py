from Foundation.Task.Task import Task
from Foundation.TaskManager import TaskManager

class TaskChainCancel(Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskChainCancel, self)._onParams(params)

        self.id = params.get("ID")
        pass

    def _onRun(self):
        if TaskManager.existTaskChain(self.id) is False:
            return True
            pass

        TaskManager.cancelTaskChain(self.id)

        return True
        pass
    pass