from Foundation.Task.MixinObjectTemplate import MixinMovieButton
from Foundation.Task.MixinObserver import MixinObserver
from Foundation.Task.Task import Task

class TaskMovieButtonLeave(MixinMovieButton, MixinObserver, Task):
    def _onParams(self, params):
        super(TaskMovieButtonLeave, self)._onParams(params)
        pass

    def _onRun(self):
        self.addObserverFilter(Notificator.onMovieButtonMouseLeave, self._onMovieButtonLeave, self.MovieButton)
        return False
        pass

    def _onMovieButtonLeave(self, movieButton):
        return True
        pass

    pass