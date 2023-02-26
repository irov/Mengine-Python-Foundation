from GOAP2.Task.TaskMovie2SocketBase import TaskMovie2SocketBase

class TaskMovie2SocketEnter(TaskMovie2SocketBase):
    def _onParams(self, params):
        super(TaskMovie2SocketEnter, self)._onParams(params)

        self.isMouseEnter = params.get("isMouseEnter", True)

        self.Button = params.get("Button", 0)
        self.isDown = params.get("isDown", None)
        pass

    def _onCheck(self):
        if self.isMouseEnter is False:
            return True
            pass

        Enable = self.Movie2.getEnable()

        if self.AutoEnable is True and Enable is False:
            self.Movie2.setEnable(True)
            pass

        MovieEntity = self.Movie2.getEntity()

        if self.Any is False and MovieEntity.isSocketMouseEnter(self.SocketName) is True:
            if self.AutoEnable is True and Enable is False:
                self.Movie2.setEnable(False)
                pass

            return False
            pass
        elif self.Any is True and MovieEntity.isAnySocketMouseEnter() is True:
            if self.AutoEnable is True and Enable is False:
                self.Movie2.setEnable(False)
                pass

            return False
            pass

        return True
        pass

    def _onRun(self):
        super(TaskMovie2SocketEnter, self)._onRun()

        def __onSocketFilter(object, name, hotspot, x, y):
            if self._onBaseFilter(name) is False:
                return False
                pass

            if self.isDown is not None:
                if Menge.isMouseButtonDown(self.Button) != self.isDown:
                    return False

            return True
            pass

        self.addEvent(self.Movie2.onMovieSocketEnterEvent, __onSocketFilter)

        return False
        pass
    pass