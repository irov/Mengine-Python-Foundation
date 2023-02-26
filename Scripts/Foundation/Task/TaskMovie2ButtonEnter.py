from Foundation.Task.MixinObjectTemplate import MixinMovie2Button
from Foundation.Task.MixinObserver import MixinObserver
from Foundation.Task.Task import Task

class TaskMovie2ButtonEnter(MixinMovie2Button, MixinObserver, Task):
    def _onParams(self, params):
        super(TaskMovie2ButtonEnter, self)._onParams(params)

        self.isMouseEnter = params.get("isMouseEnter", True)

    def _onCheck(self):
        if self.isMouseEnter is False:
            return True
            pass

        EntityMovie2Button = self.Movie2Button.getEntity()

        movie = EntityMovie2Button.getCurrentMovie()

        if movie is None:
            return True
            pass

        if movie is not None:
            socket = movie.getSocket('socket')

            if socket.isMousePickerOver() is True:
                return False
                pass
            pass

        return True
        pass

    def _onRun(self):
        self.addObserverFilter(Notificator.onMovie2ButtonMouseEnter, self._onMovie2ButtonEnter, self.Movie2Button)
        return False

    def _onMovie2ButtonEnter(self, movie2Button):
        return True