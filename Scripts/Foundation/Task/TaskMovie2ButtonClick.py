from Foundation.ArrowManager import ArrowManager
from Foundation.Task.MixinObjectTemplate import MixinMovie2Button
from Foundation.Task.MixinObserver import MixinObserver
from Foundation.Task.Task import Task

class TaskMovie2ButtonClick(MixinMovie2Button, MixinObserver, Task):
    def _onParams(self, params):
        super(TaskMovie2ButtonClick, self)._onParams(params)
        pass

    def _onRun(self):
        self.addObserverFilter(Notificator.onMovie2ButtonClick, self._onMovie2ButtonClick, self.Movie2Button)

        return False
        pass

    def _onMovie2ButtonClick(self, movie2Button):
        if ArrowManager.emptyArrowAttach() is False:
            return False
            pass

        return True
        pass

    pass