from Foundation.Task.MixinObject import MixinObject
from Foundation.Task.Task import Task

class TaskObjectSetAlpha(MixinObject, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskObjectSetAlpha, self)._onParams(params)

        self.Value = params.get("Value")
        pass

    def _onInitialize(self):
        super(TaskObjectSetAlpha, self)._onInitialize()

        if _DEVELOPMENT is True:
            if self.Value is None:
                self.initializeFailed("Alpha not initialized")
                pass
            pass
        pass

    def _onRun(self):
        self.Object.setAlpha(self.Value)

        return True
        pass
    pass