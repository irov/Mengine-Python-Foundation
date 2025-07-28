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

        def __onHandleMouseButtonEvent(context, event):
            Handle = self.Socket.getDefaultHandle()

            if self.Button != event.button:
                return Handle

            if self.isDown is not event.isDown:
                return Handle

            if self.isPressed is not None:
                if self.isDown is False and self.isPressed is not event.isPressed:
                    return Handle
                pass

            if self._onBaseFilter(event.touchId, event.position.world.x, event.position.world.y, event.button, event.isDown, event.isPressed) is False:
                return Handle

            Notification.notify(Notificator.onNodeSocketClickSuccess, self.Socket, event.touchId, event.position.world.x, event.position.world.y, event.button, event.isDown, event.isPressed)

            self.complete()

            return Handle

        self.Socket.setEventListener(onHandleMouseButtonEvent=__onHandleMouseButtonEvent)

        return False
        pass

    def _onFinally(self):
        super(TaskNodeSocketClick, self)._onFinally()

        self.Socket.setEventListener(onHandleMouseButtonEvent=None)
        pass
    pass