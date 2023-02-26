from Foundation.Task.MixinObjectTemplate import MixinButton
from Foundation.Task.Task import Task

class TaskButtonSwitchMode(MixinButton, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskButtonSwitchMode, self)._onParams(params)

        self.Value = params.get("Value")

        pass

    def _onRun(self):
        self.Button.setSwitchMode(self.Value)

        return True
        pass

    pass