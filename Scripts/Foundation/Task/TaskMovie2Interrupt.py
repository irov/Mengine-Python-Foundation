from Foundation.Task.MixinObjectTemplate import MixinMovie2
from Foundation.Task.TaskObjectAnimatableInterrupt import TaskObjectAnimatableInterrupt

class TaskMovie2Interrupt(MixinMovie2, TaskObjectAnimatableInterrupt):
    Skiped = True

    def getAnimatable(self):
        return self.Movie2
        pass