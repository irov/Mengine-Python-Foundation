from Foundation.ArrowManager import ArrowManager
from Foundation.Task.MixinEvent import MixinEvent
from Foundation.Task.MixinObjectTemplate import MixinMovie2
from Foundation.Task.Task import Task

class TaskMovie2SocketBase(MixinMovie2, MixinEvent, Task):
    def _onParams(self, params):
        super(TaskMovie2SocketBase, self)._onParams(params)

        self.SocketName = params.get("SocketName", None)
        self.Socket = params.get("Socket", None)

        self.Any = params.get("Any", False)
        self.UseArrowFilter = params.get("UseArrowFilter", True)
        self.Filter = params.get("Filter", None)
        self.AutoEnable = params.get("AutoEnable", False)
        pass

    def _onValidate(self):
        super(TaskMovie2SocketBase, self)._onValidate()

        if self.SocketName is None and self.Socket is not None:
            self.SocketName = self.Socket.getName()

        if self.Any is False and self.SocketName is None:
            self.validateFailed("SocketName is None")
            pass

        Enable = self.Movie2.getEnable()

        if Enable is False and self.AutoEnable is False:
            self.validateFailed("Movie2 %s is Disable" % (self.Movie2.getName()))
            pass
        pass

    def _onBaseFilter(self, name):
        if self.Any is True:
            return True
            pass

        if self.SocketName != name:
            return False
            pass

        if self.UseArrowFilter is True:
            if ArrowManager.emptyArrowAttach() is False:
                return False
                pass
            pass

        if self.Filter is not None:
            if self.Filter() is False:
                return False
                pass
            pass

        return True
        pass

    def _onRun(self):
        super(TaskMovie2SocketBase, self)._onRun()

        if self.AutoEnable is True:
            self.Movie2.setEnable(True)
            pass

        self.Movie2.setInteractive(True)
        pass

    def _onFinally(self):
        super(TaskMovie2SocketBase, self)._onFinally()

        self.Movie2.setInteractive(False)

        if self.AutoEnable is True:
            self.Movie2.setEnable(False)
            pass
        pass
    pass