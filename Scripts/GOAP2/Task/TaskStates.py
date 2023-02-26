from GOAP2.Task.MixinObjectTemplate import MixinStates
from GOAP2.Task.Task import Task

class TaskStates(MixinStates, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskStates, self)._onParams(params)

        self.value = params.get("Value")
        pass

    def _onInitialize(self):
        super(TaskStates, self)._onInitialize()
        pass

    def _onRun(self):
        self.States.setCurrentState(self.value)
        return True
        pass
    pass