from Foundation.Task.MixinObjectTemplate import MixinVideo
from Foundation.Task.Task import Task

class TaskVideoStop(MixinVideo, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskVideoStop, self)._onParams(params)
        pass

    def _onRun(self):
        self.Video.setParam("Play", False)
        return True
        pass
    pass