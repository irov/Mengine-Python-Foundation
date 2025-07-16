from Foundation.Task.MixinObject import MixinObject
from Foundation.Task.TaskObjectAnimatableInterrupt import TaskObjectAnimatableInterrupt

class TaskObjectInterrupt(MixinObject, TaskObjectAnimatableInterrupt):
    Skiped = True

    def getAnimatable(self):
        return self.Object
        pass
    pass