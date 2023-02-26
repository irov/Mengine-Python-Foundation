from GOAP2.Task.MixinObject import MixinObject
from GOAP2.Task.Task import Task

class TaskObjectReturn(MixinObject, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskObjectReturn, self)._onParams(params)
        pass

    def _onRun(self):
        self.Object.returnToParent()

        return True
        pass
    pass