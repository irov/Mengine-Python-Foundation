from GOAP2.Task.TaskNodeSocketBase import TaskNodeSocketBase

class TaskNodeSocketMove(TaskNodeSocketBase):
    def _onParams(self, params):
        super(TaskNodeSocketMove, self)._onParams(params)

        self.Tracker = Utils.make_functor(params, "Tracker", "TrackerArgs", "TrackerKwds")
        pass

    def _onValidate(self):
        super(TaskNodeSocketMove, self)._onValidate()

        if callable(self.Tracker) is False:
            self.validateFailed("Tracker is uncallable %s" % (self.Tracker))
            pass
        pass

    def _onRun(self):
        super(TaskNodeSocketMove, self)._onRun()

        def __onHandleMouseMove(touchId, x, y, dx, dy, pressure):
            Handle = self.Socket.getDefaultHandle()

            if self._onBaseFilter(touchId, x, y, dx, dy) is False:
                return Handle
                pass

            if self.Tracker(touchId, x, y, dx, dy) is False:
                return Handle
                pass

            self.complete()

            return Handle
            pass

        self.Socket.setEventListener(onHandleMouseMove=__onHandleMouseMove)

        return False
        pass

    def _onFinally(self):
        super(TaskNodeSocketMove, self)._onFinally()

        self.Socket.setEventListener(onHandleMouseMove=None)
        pass
    pass