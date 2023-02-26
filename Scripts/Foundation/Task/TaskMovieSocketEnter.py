from Foundation.Task.TaskMovieSocketBase import TaskMovieSocketBase

class TaskMovieSocketEnter(TaskMovieSocketBase):
    def _onParams(self, params):
        super(TaskMovieSocketEnter, self)._onParams(params)

        self.isMouseEnter = params.get("isMouseEnter", True)
        pass

    def _onCheck(self):
        if self.isMouseEnter is False:
            return True
            pass

        Enable = self.Movie.getEnable()

        if self.AutoEnable is True and Enable is False:
            self.Movie.setEnable(True)
            pass

        MovieEntity = self.Movie.getEntity()

        if self.Any is False and MovieEntity.isSocketMouseEnter(self.SocketName) is True:
            if self.AutoEnable is True and Enable is False:
                self.Movie.setEnable(False)
                pass

            return False
            pass
        elif self.Any is True and MovieEntity.isAnySocketMouseEnter() is True:
            if self.AutoEnable is True and Enable is False:
                self.Movie.setEnable(False)
                pass

            return False
            pass

        return True
        pass

    def _onRun(self):
        super(TaskMovieSocketEnter, self)._onRun()

        def __onSocketFilter(object, name, hotspot, x, y):
            if self._onBaseFilter(name) is False:
                return False
                pass

            return True
            pass

        self.addEvent(self.Movie.onMovieSocketEnterEvent, __onSocketFilter)

        return False
        pass
    pass