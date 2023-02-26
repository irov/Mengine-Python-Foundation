from Foundation.Task.Task import Task

from HOPA.TransitionManager import TransitionManager

class TaskTransitionBlock(Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskTransitionBlock, self)._onParams(params)

        self.Value = params.get("Value")
        self.IsGameScene = params.get("IsGameScene")
        pass

    def _onRun(self):
        TransitionManager.blockTransition(self.Value, self.IsGameScene)

        return True
        pass
    pass