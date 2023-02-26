from GOAP2.Task.MixinObject import MixinObject
from GOAP2.Task.Task import Task

class TaskBlockInteractive(MixinObject, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskBlockInteractive, self)._onParams(params)

        self.value = params.get("BlockInteractive", True)
        pass

    def _onInitialize(self):
        super(TaskBlockInteractive, self)._onInitialize()
        pass

    def _onRun(self):
        self.Object.setBlockInteractive(self.value)

        return True
        pass
    pass