from GOAP2.Task.MixinObject import MixinObject
from GOAP2.Task.Task import Task

class TaskAppendParam(MixinObject, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskAppendParam, self)._onParams(params)

        self.param = params.get("Param")
        self.value = params.get("Value")
        pass

    def _onInitialize(self):
        super(TaskAppendParam, self)._onInitialize()
        pass

    def _onRun(self):
        self.Object.appendParam(self.param, self.value)

        return True
        pass
    pass