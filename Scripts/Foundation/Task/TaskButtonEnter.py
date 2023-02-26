from Foundation.Task.MixinObjectTemplate import MixinButton
from Foundation.Task.MixinObserver import MixinObserver
from Foundation.Task.Task import Task

class TaskButtonEnter(MixinButton, MixinObserver, Task):
    def _onParams(self, params):
        super(TaskButtonEnter, self)._onParams(params)

        self.AutoEnable = params.get("AutoEnable", False)
        pass

    def _onCheck(self):
        if self.Button.isActive() is True:
            ButtonEntity = self.Button.getEntity()
            if ButtonEntity.isMouseEnter() is True:
                return False
                pass
            pass

        return True
        pass

    def _onRun(self):
        if self.AutoEnable is True:
            self.Button.setInteractive(True)
            pass

        self.addObserverFilter(Notificator.onButtonMouseEnter, self._onButtonMouseEnterFilter, self.Button)

        return False
        pass

    def _onButtonMouseEnterFilter(self, Button):
        return True
        pass

    def _onFinally(self):
        super(TaskButtonEnter, self)._onFinally()

        if self.AutoEnable is True:
            self.Button.setInteractive(False)
            pass
        pass

    pass