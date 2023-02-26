from Foundation.Task.MixinObject import MixinObject
from Foundation.Task.Task import Task

class TaskObjectDestroy(MixinObject, Task):
    Skiped = True

    def _onRun(self):
        self.Object.onDestroy()

        return True
        pass
    pass