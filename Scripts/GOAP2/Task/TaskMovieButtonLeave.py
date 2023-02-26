from GOAP2.Task.MixinObjectTemplate import MixinMovieButton
from GOAP2.Task.MixinObserver import MixinObserver
from GOAP2.Task.Task import Task

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