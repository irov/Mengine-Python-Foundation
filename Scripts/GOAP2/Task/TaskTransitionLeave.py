from GOAP2.Task.MixinObjectTemplate import MixinTransition
from GOAP2.Task.MixinObserver import MixinObserver
from GOAP2.Task.Task import Task

class TaskTransitionLeave(MixinTransition, MixinObserver, Task):
    def _onParams(self, params):
        super(TaskTransitionLeave, self)._onParams(params)
        pass

    def _onRun(self):
        if self.Transition.isActive() is True:
            TransitionEntity = self.Transition.getEntity()
            if TransitionEntity.isMouseEnter() is False:
                return True
                pass
            pass

        self.addObserverFilter(Notificator.onTransitionMouseLeave, self._onTransitionMouseLeaveFilter, self.Transition)

        return False
        pass

    def _onTransitionMouseLeaveFilter(self, transition):
        return True
        pass
    pass