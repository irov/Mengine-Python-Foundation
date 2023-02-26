from Foundation.ArrowManager import ArrowManager
from Foundation.Task.MixinObjectTemplate import MixinButton
from Foundation.Task.MixinObserver import MixinObserver
from Foundation.Task.Task import Task

class TaskButtonUse(MixinButton, MixinObserver, Task):
    def _onParams(self, params):
        super(TaskButtonUse, self)._onParams(params)

        self.AutoEnable = params.get("AutoEnable", True)
        pass

    def _onRun(self):
        if self.AutoEnable is True:
            self.Button.setInteractive(True)
            pass

        self.addObserverFilter(Notificator.onButtonClick, self._onButtonClick, self.Button)

        return False
        pass

    def _onFinally(self):
        super(TaskButtonUse, self)._onFinally()

        if self.AutoEnable is True:
            self.Button.setInteractive(False)
            pass
        pass

    def _onButtonClick(self, button):
        if ArrowManager.emptyArrowAttach() is True:
            return False
            pass

        return True
        pass
    pass