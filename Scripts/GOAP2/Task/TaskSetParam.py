from GOAP2.Task.MixinObject import MixinObject
from GOAP2.Task.Task import Task

class TaskSetParam(MixinObject, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskSetParam, self)._onParams(params)

        self.Param = params.get("Param")
        self.Value = params.get("Value")
        pass

    def _onInitialize(self):
        super(TaskSetParam, self)._onInitialize()
        pass

    def _onRun(self):
        self.Object.setParam(self.Param, self.Value)

        return True
        pass
    pass