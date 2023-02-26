from Foundation.Task.TaskMovie2SocketBase import TaskMovie2SocketBase

class TaskMovie2SocketClick(TaskMovie2SocketBase):
    def _onParams(self, params):
        super(TaskMovie2SocketClick, self)._onParams(params)

        self.Button = params.get("Button", 0)
        self.isDown = params.get("isDown", False)
        self.Already = params.get("Already", False)
        self.isPressed = params.get("isPressed", True)
        pass

    def _onCheck(self):
        if self.Already is False:
            return True
            pass

        if self.Movie2.hasEntity() is False:
            return True
            pass

        if self.isDown is True:
            MovieEntity = self.Movie2.getEntity()

            if self.Any is False:
                if MovieEntity.isSocketMouseEnter(self.SocketName) is False:
                    return True
                    pass
            else:
                if MovieEntity.isAnySocketMouseEnter() is False:
                    return True
                    pass
                pass

            if Mengine.isMouseButtonDown(self.Button) is False:
                return True
                pass

            return False
            pass
        else:
            MovieEntity = self.Movie2.getEntity()

            if self.Any is False:
                if MovieEntity.isSocketMouseEnter(self.SocketName) is False:
                    return True
                    pass
                pass
            else:
                if MovieEntity.isAnySocketMouseEnter() is False:
                    return True
                    pass
                pass

            if Mengine.isMouseButtonDown(self.Button) is True:
                return True
                pass

            return False
            pass

        return True
        pass

    def _onRun(self):
        super(TaskMovie2SocketClick, self)._onRun()

        def __onSocketFilter(object, name, hotspot, touchId, x, y, button, isDown, isPressed):
            if self.Button != button:
                return False
                pass

            if self.isDown is not isDown:
                return False
                pass

            if self.isDown is False and self.isPressed is not isPressed:
                return False
                pass

            if self._onBaseFilter(name) is False:
                return False
                pass

            Notification.notify(Notificator.onMovieSocketClickSuccessful, object, name, touchId, x, y, button, isDown, isPressed)
            return True
            pass

        self.addEvent(self.Movie2.onMovieSocketButtonEvent, __onSocketFilter)

        return False
        pass
    pass