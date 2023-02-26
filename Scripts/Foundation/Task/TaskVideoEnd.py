from Foundation.Task.MixinObjectTemplate import MixinVideo
from Foundation.Task.MixinObserver import MixinObserver
from Foundation.Task.Task import Task

class TaskVideoEnd(MixinVideo, MixinObserver, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskVideoEnd, self)._onParams(params)
        pass

    def _onRun(self):
        self.addObserverFilter(Notificator.onVideoEnd, self._onVideoEndFilter, self.Video)

        return False
        pass

    def _onVideoEndFilter(self, video):
        return True
        pass
    pass