from Foundation.Task.TaskNodeSocketBase import TaskNodeSocketBase

class TaskNodeSocketMove(TaskNodeSocketBase):
    def _onParams(self, params):
        super(TaskNodeSocketMove, self)._onParams(params)

        self.Tracker = Utils.make_functor(params, "Tracker", "TrackerArgs", "TrackerKwargs")
        pass

    def _onValidate(self):
        super(TaskNodeSocketMove, self)._onValidate()

        if callable(self.Tracker) is False:
            self.validateFailed("Tracker is uncallable %s" % (self.Tracker))
            pass
        pass

    def _onRun(self):
        super(TaskNodeSocketMove, self)._onRun()

        def __onHandleMouseMove(context, event):
            handle = self.Socket.getDefaultHandle()

            if self._onBaseFilter(event.touchId, event.x, event.y, event.dx, event.dy) is False:
                return handle

            if self.Tracker(event.touchId, event.x, event.y, event.dx, event.dy) is False:
                return handle

            self.complete()

            return handle

        self.Socket.setEventListener(onHandleMouseMove=__onHandleMouseMove)

        return False

    def _onFinally(self):
        super(TaskNodeSocketMove, self)._onFinally()

        self.Socket.setEventListener(onHandleMouseMove=None)
        pass
    pass