from Foundation.ArrowManager import ArrowManager
from Foundation.Task.MixinObjectTemplate import MixinButton
from Foundation.Task.MixinObserver import MixinObserver
from Foundation.Task.Task import Task

class TaskButtonClick(MixinButton, MixinObserver, Task):
    def _onParams(self, params):
        super(TaskButtonClick, self)._onParams(params)

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
        super(TaskButtonClick, self)._onFinally()

        if self.AutoEnable is True:
            self.Button.setInteractive(False)
            pass
        pass

    def _onButtonClick(self, button):
        if ArrowManager.emptyArrowAttach() is False:
            return False
            pass

        return True
        pass

    pass