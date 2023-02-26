from GOAP2.Task.Task import Task

class TaskNodeSocketBase(Task):
    def _onParams(self, params):
        super(TaskNodeSocketBase, self)._onParams(params)

        self.Socket = params.get("Socket")
        self.Filter = Utils.make_functor(params, "Filter")

        self.AutoEnable = params.get("AutoEnable", False)
        pass

    def _onValidate(self):
        super(TaskNodeSocketBase, self)._onValidate()

        if self.Socket is None:
            self.validateFailed("Socket is None")
            pass

        if Menge.isHomeless(self.Socket) is True:
            self.validateFailed("Socket %s is Homeless" % (self.Socket.getName()))
            pass
        pass

    def _onBaseFilter(self, *args):
        if self.Filter is not None:
            if self.Filter(*args) is False:
                return False
                pass
            pass

        return True
        pass

    def _onRun(self):
        super(TaskNodeSocketBase, self)._onRun()

        if self.AutoEnable is True:
            self.Socket.enable()
            pass
        pass

    def _onFinally(self):
        super(TaskNodeSocketBase, self)._onFinally()

        if self.AutoEnable is True:
            self.Socket.disable()
            pass
        pass
    pass