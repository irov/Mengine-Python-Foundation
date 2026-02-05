from Foundation.Task.MixinObject import MixinObject
from Foundation.Task.Task import Task

class TaskDestroy(MixinObject, Task):
    Skiped = True

    def _onRun(self):
        self.Object.onDestroy()

        return True
    pass