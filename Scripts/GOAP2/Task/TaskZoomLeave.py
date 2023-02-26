from GOAP2.Task.MixinObserver import MixinObserver
from GOAP2.Task.MixinZoomGroup import MixinZoomGroup
from GOAP2.Task.Task import Task
from GOAP3.ZoomManager import ZoomManager

class TaskZoomLeave(MixinZoomGroup, MixinObserver, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskZoomLeave, self)._onParams(params)
        self.ZoomAny = params.get("ZoomAny", False)
        pass

    def _onCheck(self):
        if self.ZoomAny is False:
            if self.isZoomLeave() is True:
                return False
                pass
            pass
        else:
            if ZoomManager.isZoomEmpty() is True:
                return False
                pass
            pass

        return True
        pass

    def _onRun(self):
        if self.ZoomAny is False:
            self.addObserver(Notificator.onZoomLeave, self._onZoomFilter)
            return False
            pass

        self.addObserver(Notificator.onZoomLeave, self._onZoomAny)
        return False
        pass
    pass