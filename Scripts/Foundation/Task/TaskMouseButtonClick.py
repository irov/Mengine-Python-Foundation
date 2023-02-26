from Foundation.Task.MixinObserver import MixinObserver
from Foundation.Task.Task import Task

class TaskMouseButtonClick(MixinObserver, Task):
    def onParams(self, params):
        super(TaskMouseButtonClick, self).onParams(params)

        self.Button = params.get("Button", 0)
        self.isDown = params.get("isDown", False)
        pass

    def _onRun(self):
        self.addObserver(Notificator.onMouseButtonEvent, self._onMouseButtonEvent)

        return False
        pass

    def _onMouseButtonEvent(self, event):
        if self.Button != event.button:
            return False
            pass

        if self.isDown is not event.isDown:
            return False
            pass

        return True
        pass
    pass