from Foundation.Task.MixinObjectTemplate import MixinButton
from Foundation.Task.Task import Task

class TaskButtonBlockState(MixinButton, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskButtonBlockState, self)._onParams(params)

        self.Value = params.get("Value")

        pass

    def _onRun(self):
        self.Button.setBlockState(self.Value)

        return True
        pass

    pass