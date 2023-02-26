from GOAP2.Task.MixinObject import MixinObject
from GOAP2.Task.Task import Task

class TaskEnable(MixinObject, Task):
    __metaclass__ = finalslots("value")

    Skiped = True

    def _onParams(self, params):
        super(TaskEnable, self)._onParams(params)

        self.value = params.get("Value", True)
        pass

    def _onInitialize(self):
        super(TaskEnable, self)._onInitialize()
        pass

    def _onRun(self):
        self.Object.setEnable(self.value)

        return True
        pass
    pass