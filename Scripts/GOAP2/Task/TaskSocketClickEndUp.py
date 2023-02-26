from GOAP2.ArrowManager import ArrowManager
from GOAP2.Task.MixinObjectTemplate import MixinSocket
from GOAP2.Task.MixinObserver import MixinObserver
from GOAP2.Task.Task import Task

class TaskSocketClickEndUp(MixinSocket, MixinObserver, Task):
    def _onParams(self, params):
        super(TaskSocketClickEndUp, self)._onParams(params)
        self.AutoEnable = params.get("AutoEnable", False)
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

        self.addObserverFilter(Notificator.onSocketClickEndUp, __onSocketFilter, self.Socket)

        return False
        pass

    def _onFinally(self):
        super(TaskSocketClickEndUp, self)._onFinally()

        if self.AutoEnable is True:
            self.Socket.setInteractive(False)
            pass
        pass
    pass