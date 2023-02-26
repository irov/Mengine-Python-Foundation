from GOAP2.Task.MixinObject import MixinObject
from GOAP2.Task.Task import Task

class TaskDelParam(MixinObject, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskDelParam, self)._onParams(params)

        self.param = params.get("Param")
        self.value = params.get("Value")

    def _onInitialize(self):
        super(TaskDelParam, self)._onInitialize()

    def _onRun(self):
        param = self.Object.getParam(self.param)

        if self.value not in param:
            Trace.log("Task", 0, "TaskDelParam: Value {!r} not in param {!r} of object {!r} | values={}".format(self.value, self.param, self.Object, param))
            return True

        self.Object.delParam(self.param, self.value)

        return True