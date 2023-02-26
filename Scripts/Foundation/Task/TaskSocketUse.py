from Foundation.ArrowManager import ArrowManager
from Foundation.Task.MixinObjectTemplate import MixinSocket
from Foundation.Task.MixinObserver import MixinObserver
from Foundation.Task.Task import Task

class TaskSocketUse(MixinSocket, MixinObserver, Task):
    def _onParams(self, params):
        super(TaskSocketUse, self)._onParams(params)

        self.AutoEnable = params.get("AutoEnable", True)
        pass

    def _onRun(self):
        if self.AutoEnable is True:
            self.Socket.setInteractive(True)
            pass

        self.addObserverFilter(Notificator.onSocketClick, self._onSocketFilter, self.Socket)

        return False
        pass

    def _onFinally(self):
        super(TaskSocketUse, self)._onFinally()

        if self.AutoEnable is True:
            self.Socket.setInteractive(False)
            pass
        pass

    def _onSocketFilter(self, socket):
        if ArrowManager.emptyArrowAttach() is True:
            return False
            pass

        return True
        pass
    pass