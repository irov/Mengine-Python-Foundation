from Foundation.ArrowManager import ArrowManager
from Foundation.Task.MixinObjectTemplate import MixinSocket
from Foundation.Task.MixinObserver import MixinObserver
from Foundation.Task.Task import Task

class TaskSocketClick(MixinSocket, MixinObserver, Task):
    def _onParams(self, params):
        super(TaskSocketClick, self)._onParams(params)

        self.AutoEnable = params.get("AutoEnable", True)
        pass

    def _onRun(self):
        if self.AutoEnable is True:
            self.Socket.setInteractive(True)
            pass

        def __onSocketFilter(socket):
            if ArrowManager.emptyArrowAttach() is False:
                return False
                pass

            return True
            pass

        self.addObserverFilter(Notificator.onSocketClick, __onSocketFilter, self.Socket)

        return False
        pass

    def _onFinally(self):
        super(TaskSocketClick, self)._onFinally()

        if self.AutoEnable is True:
            self.Socket.setInteractive(False)
            pass
        pass
    pass