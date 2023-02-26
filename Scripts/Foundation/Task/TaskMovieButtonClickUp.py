from Foundation.ArrowManager import ArrowManager
from Foundation.Task.MixinObjectTemplate import MixinMovieButton
from Foundation.Task.MixinObserver import MixinObserver
from Foundation.Task.Task import Task

class TaskMovieButtonClickUp(MixinMovieButton, MixinObserver, Task):
    def _onParams(self, params):
        super(TaskMovieButtonClickUp, self)._onParams(params)
        pass

    def _onRun(self):
        self.addObserverFilter(Notificator.onMovieButtonClickUp, self._onMovieButtonClickUp, self.MovieButton)
        return False
        pass

    def _onMovieButtonClickUp(self, movieButton):
        if ArrowManager.emptyArrowAttach() is False:
            return False
            pass

        return True
        pass

    pass