from GOAP2.Task.MixinObjectTemplate import MixinAnimation
from GOAP2.Task.Task import Task

class TaskAnimationSetSequence(MixinAnimation, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskAnimationSetSequence, self)._onParams(params)

        self.Sequence = params.get("Sequence")
        pass

    def _onRun(self):
        self.Animation.setSequence(self.Sequence)

        return True
        pass
    pass