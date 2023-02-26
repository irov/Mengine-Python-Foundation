from GOAP2.Task.MixinObjectTemplate import MixinCheckBoxAlias
from GOAP2.Task.Task import Task

class TaskCheckBoxBlockState(MixinCheckBoxAlias, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskCheckBoxBlockState, self)._onParams(params)

        self.Value = params.get("Value")
        pass

    def _onRun(self):
        self.CheckBox.setBlockState(self.Value)

        return True
        pass
    pass