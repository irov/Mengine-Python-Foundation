from Foundation.Task.TaskNodeSocketBase import TaskNodeSocketBase

class TaskNodeSocketEnter(TaskNodeSocketBase):
    def _onParams(self, params):
        super(TaskNodeSocketEnter, self)._onParams(params)

        self.isMouseEnter = params.get("isMouseEnter", True)
        pass

    def _onCheck(self):
        if self.isMouseEnter is False:
            return True

        Enable = self.Socket.isEnable()

        if self.AutoEnable is True and Enable is False:
            self.Socket.enable()
            pass

        pick = self.Socket.isMousePickerOver()

        if self.AutoEnable is True and Enable is False:
            self.Socket.disable()
            pass

        if pick is True:
            return False

        return True

    def _onRun(self):
        super(TaskNodeSocketEnter, self)._onRun()

        def __onHandleMouseEnter(context, event):
            handle = self.Socket.getDefaultHandle()

            if self._onBaseFilter() is False:
                return handle

            self.complete()

            return handle

        self.Socket.setEventListener(onHandleMouseEnter=__onHandleMouseEnter)

        return False

    def _onFinally(self):
        super(TaskNodeSocketEnter, self)._onFinally()

        if self.Socket is None:
            return

        self.Socket.setEventListener(onHandleMouseEnter = None)
        pass
    pass