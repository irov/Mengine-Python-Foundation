from GOAP2.Task.MixinObject import MixinObject
from GOAP2.Task.Task import Task

class TaskChangeParam(MixinObject, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskChangeParam, self)._onParams(params)

        self.param = params.get("Param")
        self.keyId = params.get("KeyID")
        self.value = params.get("Value")
        pass

    def _onInitialize(self):
        super(TaskChangeParam, self)._onInitialize()
        pass

    def _onRun(self):
        self.Object.changeParam(self.param, self.keyId, self.value)

        return True
        pass
    pass