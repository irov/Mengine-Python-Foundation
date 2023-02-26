from Foundation.ArrowManager import ArrowManager
from Foundation.Task.MixinObjectTemplate import MixinMovieButton
from Foundation.Task.MixinObserver import MixinObserver
from Foundation.Task.Task import Task

class TaskMovieButtonUse(MixinMovieButton, MixinObserver, Task):
    def _onParams(self, params):
        super(TaskMovieButtonUse, self)._onParams(params)
        pass

    def _onRun(self):
        self.addObserverFilter(Notificator.onMovieButtonClick, self._onMovieButtonClick, self.MovieButton)

        return False
        pass

    def _onMovieButtonClick(self, movieButton):
        if ArrowManager.emptyArrowAttach() is True:
            return False
            pass

        return True
        pass
    pass