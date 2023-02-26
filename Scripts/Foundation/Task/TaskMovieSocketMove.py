from Foundation.Task.TaskMovieSocketBase import TaskMovieSocketBase

class TaskMovieSocketMove(TaskMovieSocketBase):
    def _onParams(self, params):
        super(TaskMovieSocketMove, self)._onParams(params)

        self.Tracker = params.get("Tracker")
        pass

    def _onValidate(self):
        super(TaskMovieSocketMove, self)._onValidate()

        if callable(self.Tracker) is False:
            self.validateFailed("Tracker is uncallable %s" % (self.Tracker))
            pass
        pass

    def _onRun(self):
        super(TaskMovieSocketMove, self)._onRun()

        def __onMovieSocketMove(object, name, hotspot, touchId, x, y, dx, dy):
            if self._onBaseFilter(name) is False:
                return False
                pass

            isComplete = self.Tracker(touchId, x, y, dx, dy)

            return isComplete
            pass

        self.addEvent(self.Movie.onMovieSocketMoveEvent, __onMovieSocketMove)

        return False
        pass
    pass