from GOAP2.Task.MixinObjectTemplate import MixinAnimation
from GOAP2.Task.Task import Task

class TaskAnimationSetFrame(MixinAnimation, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskAnimationSetFrame, self)._onParams(params)
        self.Frame = params.get("Frame")
        pass

    def _onRun(self):
        self.Animation.setFrameIndex(self.Frame)

        return True
        pass
    pass