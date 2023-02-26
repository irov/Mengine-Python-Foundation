from GOAP2.Task.MixinObject import MixinObject
from GOAP2.Task.Task import Task

class TaskObjectDeactivate(MixinObject, Task):
    Skiped = True

    def _onRun(self):
        self.Object.onDeactivate()

        return True
        pass
    pass