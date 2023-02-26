from Foundation.Task.MixinObject import MixinObject
from Foundation.Task.TaskObjectAnimatablePlay import TaskObjectAnimatablePlay

class TaskObjectPlay(MixinObject, TaskObjectAnimatablePlay):
    Skiped = True

    def getAnimatable(self):
        return self.Object
        pass
    pass