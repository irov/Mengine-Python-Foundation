from Foundation.Task.MixinObjectTemplate import MixinButton
from Foundation.Task.Task import Task

class TaskButtonChangeState(MixinButton, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskButtonChangeState, self)._onParams(params)

        self.NewState = params.get("NewState")
        self.BlockState = params.get("BlockState", False)
        pass

    def _onRun(self):
        curState = self.Button.getState()

        if curState == self.NewState:
            return True
            pass

        # if self.BlockState is False:
        #     self.Button.setBlockState(self.BlockState)
        #     pass

        self.Button.setState(self.NewState)
        # if self.BlockState is True:
        #     self.Button.setBlockState(self.BlockState)
        #     pass

        return True
        pass

    pass