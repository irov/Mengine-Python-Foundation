from Foundation.Task.MixinObject import MixinObject
from Foundation.Task.Task import Task

class TaskObjectDeactivate(MixinObject, Task):
    Skiped = True

    def _onRun(self):
        self.Object.onDeactivate()

        return True
        pass
    pass