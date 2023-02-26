from Foundation.Task.TaskNodeSocketBase import TaskNodeSocketBase

class TaskNodeSocketClick(TaskNodeSocketBase):
    def _onParams(self, params):
        super(TaskNodeSocketClick, self)._onParams(params)

        self.Button = params.get("Button", 0)
        self.isDown = params.get("isDown", False)
        self.isPressed = params.get("isPressed", True)
        pass

    def _onRun(self):
        super(TaskNodeSocketClick, self)._onRun()

        def __onHandleMouseButtonEvent(touchId, x, y, button, pressure, isDown, isPressed):
            Handle = self.Socket.getDefaultHandle()

            if self.Button != button:
                return Handle
                pass

            if self.isDown is not isDown:
                return Handle
                pass

            if self.isPressed is not None:
                if self.isDown is False and self.isPressed is not isPressed:
                    return Handle
                    pass
                pass

            if self._onBaseFilter(touchId, x, y, button, isDown, isPressed) is False:
                return Handle
                pass

            Notification.notify(Notificator.onNodeSocketClickSuccessful, self.Socket, touchId, x, y, button, isDown, isPressed)

            self.complete()

            return Handle
            pass

        self.Socket.setEventListener(onHandleMouseButtonEvent=__onHandleMouseButtonEvent)

        return False
        pass

    def _onFinally(self):
        super(TaskNodeSocketClick, self)._onFinally()

        self.Socket.setEventListener(onHandleMouseButtonEvent=None)
        pass
    pass