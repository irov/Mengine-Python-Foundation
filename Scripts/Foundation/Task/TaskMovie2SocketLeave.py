from Foundation.Task.TaskMovie2SocketBase import TaskMovie2SocketBase

class TaskMovie2SocketLeave(TaskMovie2SocketBase):
    def _onParams(self, params):
        super(TaskMovie2SocketLeave, self)._onParams(params)

        self.isMouseLeave = params.get("isMouseLeave", True)
        pass

    def _onCheck(self):
        if self.isMouseLeave is False:
            return True
            pass

        Enable = self.Movie2.getEnable()

        if self.AutoEnable is True and Enable is False:
            self.Movie2.setEnable(True)
            pass

        MovieEntity = self.Movie2.getEntity()

        if self.Any is False and MovieEntity.isSocketMouseEnter(self.SocketName) is False:
            if self.AutoEnable is True and Enable is False:
                self.Movie2.setEnable(False)
                pass

            return False
            pass
        elif self.Any is True and MovieEntity.isAnySocketMouseEnter() is False:
            if self.AutoEnable is True and Enable is False:
                self.Movie2.setEnable(False)
                pass

            return False
            pass

        return True
        pass

    def _onRun(self):
        super(TaskMovie2SocketLeave, self)._onRun()

        def __onSocketFilter(object, name, hotspot):
            if self._onBaseFilter(name) is False:
                return False
                pass

            return True
            pass

        self.addEvent(self.Movie2.onMovieSocketLeaveEvent, __onSocketFilter)

        return False
        pass
    pass