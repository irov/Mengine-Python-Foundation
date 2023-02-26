from Foundation.Task.Task import Task
from Foundation.TaskManager import TaskManager

class TaskChainRun(Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskChainRun, self)._onParams(params)
        self.id = params.get("ID")
        pass

    def _onRun(self):
        TaskManager.runTaskChain(self.id)

        return True
        pass
    pass