from GOAP2.Task.MixinObject import MixinObject
from GOAP2.Task.Task import Task

class TaskInteractive(MixinObject, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskInteractive, self)._onParams(params)

        self.Value = params.get("Value", True)
        pass

    def _onInitialize(self):
        super(TaskInteractive, self)._onInitialize()
        pass

    def _onRun(self):
        self.Object.setParamInteractive(self.Value)

        return True
        pass
    pass