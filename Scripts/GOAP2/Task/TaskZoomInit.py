from GOAP2.Task.MixinObserver import MixinObserver
from GOAP2.Task.MixinZoomGroup import MixinZoomGroup
from GOAP2.Task.Task import Task

class TaskZoomInit(MixinZoomGroup, MixinObserver, Task):
    Skiped = False

    def _onCheck(self):
        if self.isZoomInit() is True:
            return False
            pass

        return True
        pass

    def _onRun(self):
        self.addObserver(Notificator.onZoomInit, self._onZoomFilter)

        return False
        pass
    pass