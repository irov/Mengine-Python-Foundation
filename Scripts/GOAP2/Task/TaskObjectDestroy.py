from GOAP2.Task.MixinObject import MixinObject
from GOAP2.Task.Task import Task

class TaskObjectDestroy(MixinObject, Task):
    Skiped = True

    def _onRun(self):
        self.Object.onDestroy()

        return True
        pass
    pass