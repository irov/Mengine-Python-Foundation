from Foundation.Task.MixinObjectTemplate import MixinTransition
from Foundation.Task.MixinObserver import MixinObserver
from Foundation.Task.Task import Task

class TaskTransitionEnter(MixinTransition, MixinObserver, Task):
    def _onParams(self, params):
        super(TaskTransitionEnter, self)._onParams(params)
        pass

    def _onRun(self):
        if self.Transition.isActive() is True:
            TransitionEntity = self.Transition.getEntity()
            if TransitionEntity.isMouseEnter() is True:
                return True
                pass
            pass

        self.addObserverFilter(Notificator.onTransitionMouseEnter, self._onTransitionMouseEnterFilter, self.Transition)

        return False
        pass

    def _onTransitionMouseEnterFilter(self, transition):
        return True
        pass
    pass