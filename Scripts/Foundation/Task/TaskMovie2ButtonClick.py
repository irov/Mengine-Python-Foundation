from Foundation.ArrowManager import ArrowManager
from Foundation.Task.MixinObjectTemplate import MixinMovie2Button
from Foundation.Task.MixinObserver import MixinObserver
from Foundation.Task.Task import Task


class TaskMovie2ButtonClick(MixinMovie2Button, MixinObserver, Task):
    def _onParams(self, params):
        super(TaskMovie2ButtonClick, self)._onParams(params)
        self.isDown = params.get("isDown", False)

    def _onRun(self):
        if self.isDown is False:
            # if you pressed (isDown=True) but remove arrow from button - it would be Leave state, not Click
            self.addObserverFilter(Notificator.onMovie2ButtonClick, self._onMovie2ButtonClick, self.Movie2Button)
        else:
            self.addObserverFilter(Notificator.onMovie2ButtonPressed, self._onMovie2ButtonClick, self.Movie2Button)

        return False

    def _onMovie2ButtonClick(self, movie2Button):
        if ArrowManager.emptyArrowAttach() is False:
            return False

        return True
