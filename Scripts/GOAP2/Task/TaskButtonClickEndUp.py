from GOAP2.ArrowManager import ArrowManager
from GOAP2.Task.MixinObjectTemplate import MixinButton
from GOAP2.Task.MixinObserver import MixinObserver
from GOAP2.Task.Task import Task

class TaskButtonClickEndUp(MixinButton, MixinObserver, Task):
    def _onParams(self, params):
        super(TaskButtonClickEndUp, self)._onParams(params)

        self.AutoEnable = params.get("AutoEnable", True)
        pass

    def _onRun(self):
        if self.AutoEnable is True:
            self.Button.setInteractive(True)
            pass

        self.addObserverFilter(Notificator.onButtonClickEndUp, self._onButtonClick, self.Button)

        return False
        pass

    def _onFinally(self):
        super(TaskButtonClickEndUp, self)._onFinally()

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