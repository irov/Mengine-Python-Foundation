from Foundation.Task.MixinObserver import MixinObserver
from Foundation.Task.Task import Task
from GOAP3.TransitionManager import TransitionManager

class TaskTransitionUnblock(MixinObserver, Task):
    Skiped = False

    def _onParams(self, params):
        super(TaskTransitionUnblock, self)._onParams(params)

        self.IsGameScene = params.get("IsGameScene")
        pass

    def _onCheck(self):
        if TransitionManager.isBlockTransition() is False:
            return False
            pass

        return True
        pass

    def _onRun(self):
        self.addObserver(Notificator.onTransitionBlock, self.__onTransitionBlockFilter)

        return False
        pass

    def __onTransitionBlockFilter(self, value, isGameScene):
        if self.IsGameScene is not isGameScene:
            return False
            pass

        if value is True:
            return False
            pass

        return True
        pass
    pass