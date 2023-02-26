from Foundation.Task.MixinObjectTemplate import MixinMovieCheckBox
from Foundation.Task.MixinObserver import MixinObserver
from Foundation.Task.Task import Task

class TaskMovieCheckBox(MixinMovieCheckBox, MixinObserver, Task):
    def _onParams(self, params):
        super(TaskMovieCheckBox, self)._onParams(params)

        self.Value = params.get("Value")
        pass

    def _onRun(self):
        self.addObserverFilter(Notificator.onMovieCheckBox, self._onMovieCheckBoxFilter, self.MovieCheckBox)

        return False
        pass

    def _onMovieCheckBoxFilter(self, checkBox, value):
        if value is not self.Value:
            return False
            pass

        return True
        pass
    pass