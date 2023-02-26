from GOAP2.Task.MixinObject import MixinObject
from GOAP2.Task.Task import Task

class TaskObjectSetScale(MixinObject, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskObjectSetScale, self)._onParams(params)

        self.Value = params.get("Value")
        pass

    def _onInitialize(self):
        super(TaskObjectSetScale, self)._onInitialize()

        if _DEVELOPMENT is True:
            if self.Value is None:
                self.initializeFailed("PositionTo not initialized")
                pass
            pass
        pass

    def _onRun(self):
        self.Object.setScale(self.Value)

        return True
        pass
    pass