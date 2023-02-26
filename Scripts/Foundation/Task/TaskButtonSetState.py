from Foundation.Task.MixinObjectTemplate import MixinButton
from Foundation.Task.Task import Task

class TaskButtonSetState(MixinButton, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskButtonSetState, self)._onParams(params)

        self.State = params.get("State")

        pass

    def _onRun(self):
        # print self.Button.getName(), self.State
        self.Button.setState(self.State)

        return True
        pass

    pass