from Foundation.Task.MixinObject import MixinObject
from Foundation.Task.Task import Task

class TaskObjectSetPosition(MixinObject, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskObjectSetPosition, self)._onParams(params)

        self.Value = params.get("Value")
        pass

    def _onInitialize(self):
        super(TaskObjectSetPosition, self)._onInitialize()

        if _DEVELOPMENT is True:
            if self.Value is None:
                self.initializeFailed("PositionTo not initialized")
                pass
            pass
        pass

    def _onRun(self):
        self.Object.setPosition(self.Value)
        return True
        pass
    pass