from GOAP2.Task.MixinObjectTemplate import MixinMovie2Button
from GOAP2.Task.MixinObserver import MixinObserver
from GOAP2.Task.Task import Task

class TaskMovie2ButtonLeave(MixinMovie2Button, MixinObserver, Task):
    def _onParams(self, params):
        super(TaskMovie2ButtonLeave, self)._onParams(params)

        self.isMouseLeave = params.get("isMouseLeave", True)

    def _onCheck(self):
        if self.isMouseLeave is False:
            return True
            pass

        EntityMovie2Button = self.Movie2Button.getEntity()

        movie = EntityMovie2Button.getCurrentMovie()

        if movie is None:
            return True
            pass

        if movie is not None:
            socket = movie.getSocket('socket')

            if socket.isMousePickerOver() is False:
                return False
                pass
            pass

        return True
        pass

    def _onRun(self):
        self.addObserverFilter(Notificator.onMovie2ButtonMouseLeave, self._onMovie2ButtonLeave, self.Movie2Button)
        return False

    def _onMovie2ButtonLeave(self, movie2Button):
        return True