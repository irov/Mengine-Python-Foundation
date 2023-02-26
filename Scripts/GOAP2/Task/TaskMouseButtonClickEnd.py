from GOAP2.Task.MixinObserver import MixinObserver
from GOAP2.Task.Task import Task

class TaskMouseButtonClickEnd(MixinObserver, Task):
    def onParams(self, params):
        super(TaskMouseButtonClickEnd, self).onParams(params)
        self.Button = params.get("Button", 0)
        self.isDown = params.get("isDown", False)

        self.Filter = Utils.make_functor(params, "Filter")
        pass

    def _onRun(self):
        self.addObserver(Notificator.onMouseButtonEventEnd, self._onMouseButtonEventEnd)

        return False
        pass

    def _onMouseButtonEventEnd(self, event):
        if self.Button != event.button:
            return False
            pass

        if self.isDown is not event.isDown:
            return False
            pass

        if self.Filter is not None:
            if self.Filter(event.touchId, event.x, event.y, event.button, event.isDown) is False:
                return False
                pass
            pass

        return True
        pass
    pass