from GOAP2.Task.MixinObjectTemplate import MixinTransition
from GOAP2.Task.MixinObserver import MixinObserver
from GOAP2.Task.Task import Task

class TaskTransitionClick(MixinTransition, MixinObserver, Task):
    def _onParams(self, params):
        super(TaskTransitionClick, self)._onParams(params)

        self.AutoEnable = params.get("AutoEnable", True)
        pass

    def _onRun(self):
        if self.AutoEnable is True:
            self.Transition.setInteractive(True)
            pass

        self.addObserverFilter(Notificator.onTransitionClick, self._onTransitionClickFilter, self.Transition)

        return False
        pass

    def _onFinally(self):
        super(TaskTransitionClick, self)._onFinally()

        if self.AutoEnable is True:
            self.Transition.setInteractive(False)
            pass
        pass

    def _onTransitionClickFilter(self, transition):
        return True
        pass
    pass