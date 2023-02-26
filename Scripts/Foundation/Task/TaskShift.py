from Foundation.Task.MixinObjectTemplate import MixinShift
from Foundation.Task.Task import Task

class TaskShift(MixinShift, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskShift, self)._onParams(params)

        self.value = params.get("Value")
        pass

    def _onInitialize(self):
        super(TaskShift, self)._onInitialize()
        pass

    def _onRun(self):
        self.Shift.setParam("Shift", self.value)
        return True
        pass
    pass