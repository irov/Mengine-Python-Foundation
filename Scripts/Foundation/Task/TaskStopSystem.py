from Foundation.Task.MixinGroup import MixinGroup
from Foundation.Task.Task import Task

class TaskStopSystem(MixinGroup, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskStopSystem, self)._onParams(params)

        self.systemName = params.get("SystemName")
        pass

    def _onRun(self):
        self.Group.stopSystem(self.systemName)
        return True
        pass
    pass