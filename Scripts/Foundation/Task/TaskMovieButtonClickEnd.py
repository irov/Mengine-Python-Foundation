from Foundation.ArrowManager import ArrowManager
from Foundation.Task.MixinObjectTemplate import MixinMovieButton
from Foundation.Task.MixinObserver import MixinObserver
from Foundation.Task.Task import Task

class TaskMovieButtonClickEnd(MixinMovieButton, MixinObserver, Task):
    def _onParams(self, params):
        super(TaskMovieButtonClickEnd, self)._onParams(params)
        pass

    def _onRun(self):
        self.addObserverFilter(Notificator.onMovieButtonClickEnd, self._onMovieButtonClickEnd, self.MovieButton)
        return False
        pass

    def _onMovieButtonClickEnd(self, movieButton):
        if ArrowManager.emptyArrowAttach() is False:
            return False
            pass

        return True
        pass

    pass