from Foundation.Task.MixinObjectTemplate import MixinButton
from Foundation.Task.Task import Task

class TaskButtonBlockKeys(MixinButton, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskButtonBlockKeys, self)._onParams(params)

        self.Value = params.get("Value")

        pass

    def _onRun(self):
        self.Button.setBlockKeys(self.Value)

        return True
        pass

    pass