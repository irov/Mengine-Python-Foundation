from GOAP2.ArrowManager import ArrowManager
from GOAP2.Task.MixinObjectTemplate import MixinMovieButton
from GOAP2.Task.MixinObserver import MixinObserver
from GOAP2.Task.Task import Task

class TaskMovieButtonPressed(MixinMovieButton, MixinObserver, Task):
    def _onParams(self, params):
        super(TaskMovieButtonPressed, self)._onParams(params)
        pass

    def _onRun(self):
        self.addObserverFilter(Notificator.onMovieButtonPressed, self._onMovieButtonPressed, self.MovieButton)
        return False
        pass

    def _onMovieButtonPressed(self, movieButton):
        if ArrowManager.emptyArrowAttach() is False:
            return False
            pass

        return True
        pass

    pass