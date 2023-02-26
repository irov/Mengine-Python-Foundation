from GOAP2.Task.MixinObjectTemplate import MixinSocket
from GOAP2.Task.MixinObserver import MixinObserver
from GOAP2.Task.Task import Task

class TaskSocketEnter(MixinSocket, MixinObserver, Task):
    def _onParams(self, params):
        super(TaskSocketEnter, self)._onParams(params)

        self.AutoEnable = params.get("AutoEnable", True)
        self.isMouseEnter = params.get("isMouseEnter", True)
        pass

    def _onRun(self):
        if self.AutoEnable is True:
            self.Socket.setInteractive(True)
            pass

        if self.isMouseEnter is True:
            if self.Socket.isActive() is True:
                SocketEntity = self.Socket.getEntity()
                if SocketEntity.isMouseEnter() is True:
                    return True
                    pass
                pass
            pass

        self.addObserverFilter(Notificator.onSocketMouseEnter, self._onSocketMouseEnterFilter, self.Socket)

        return False
        pass

    def _onFinally(self):
        super(TaskSocketEnter, self)._onFinally()

        if self.AutoEnable is True:
            self.Socket.setInteractive(False)
            pass
        pass

    def _onSocketMouseEnterFilter(self, socket):
        return True
        pass
    pass