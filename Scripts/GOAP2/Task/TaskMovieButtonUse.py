from GOAP2.ArrowManager import ArrowManager
from GOAP2.Task.MixinObjectTemplate import MixinMovieButton
from GOAP2.Task.MixinObserver import MixinObserver
from GOAP2.Task.Task import Task

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