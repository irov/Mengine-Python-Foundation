from Foundation.Task.MixinObject import MixinObject
from Foundation.Task.Task import Task

class TaskObjectActivate(MixinObject, Task):
    Skiped = True

    def _onRun(self):
        self.Object.onActivate()

        return True
        pass
    pass