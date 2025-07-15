from Foundation.Task.TaskNodeSocketBase import TaskNodeSocketBase

class TaskNodeSocketLeave(TaskNodeSocketBase):
    def _onParams(self, params):
        super(TaskNodeSocketLeave, self)._onParams(params)

        self.isMouseLeave = params.get("isMouseLeave", True)
        self.Skiped = params.get("Skiped", False)
        pass

    def _onCheck(self):
        if self.isMouseLeave is False:
            return True
            pass

        Enable = self.Socket.isEnable()

        if self.AutoEnable is True and Enable is False:
            self.Socket.enable()
            pass

        pick = self.Socket.isMousePickerOver()

        if self.AutoEnable is True and Enable is False:
            self.Socket.disable()
            pass

        if pick is False:
            return False
            pass

        return True
        pass

    def _onRun(self):
        super(TaskNodeSocketLeave, self)._onRun()

        def __onHandleMouseLeave(context, event):
            if self._onBaseFilter() is False:
                return
                pass

            self.complete()
            pass

        self.Socket.setEventListener(onHandleMouseLeave=__onHandleMouseLeave)

        return False
        pass

    def _onFinally(self):
        super(TaskNodeSocketLeave, self)._onFinally()

        if Mengine.isHomeless(self.Socket) is True:
            return

        self.Socket.setEventListener(onHandleMouseLeave=None)
        pass
    pass