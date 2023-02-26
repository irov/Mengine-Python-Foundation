from GOAP2.Task.MixinObjectTemplate import MixinMovieButton
from GOAP2.Task.MixinObserver import MixinObserver
from GOAP2.Task.Task import Task

class TaskMovieButtonEnter(MixinMovieButton, MixinObserver, Task):
    def _onParams(self, params):
        super(TaskMovieButtonEnter, self)._onParams(params)
        pass

    def _onRun(self):
        self.addObserverFilter(Notificator.onMovieButtonMouseEnter, self._onMovieButtonEnter, self.MovieButton)
        return False
        pass

    def _onMovieButtonEnter(self, movieButton):
        return True
        pass

    pass