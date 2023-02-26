from Foundation.Task.MixinObjectTemplate import MixinButton
from Foundation.Task.MixinObserver import MixinObserver
from Foundation.Task.Task import Task

class TaskButtonLeave(MixinButton, MixinObserver, Task):
    def _onParams(self, params):
        super(TaskButtonLeave, self)._onParams(params)
        self.isMouseEnter = params.get("isMouseEnter", False)
        pass

    def _onCheck(self):
        if self.isMouseEnter is False:
            return True
            pass

        if self.isMouseEnter is True:
            if self.Button.isActive() is True:
                ButtonEntity = self.Button.getEntity()
                if ButtonEntity.isMouseEnter() is False:
                    return False
                    pass
                pass
            pass

        return True
        pass

    def _onRun(self):
        self.addObserverFilter(Notificator.onButtonMouseLeave, self._onButtonMouseLeaveFilter, self.Button)

        return False
        pass

    def _onButtonMouseLeaveFilter(self, Button):
        return True
        pass
    pass