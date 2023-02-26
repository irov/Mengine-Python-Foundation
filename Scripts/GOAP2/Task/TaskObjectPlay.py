from GOAP2.Task.MixinObject import MixinObject
from GOAP2.Task.TaskObjectAnimatablePlay import TaskObjectAnimatablePlay

class TaskObjectPlay(MixinObject, TaskObjectAnimatablePlay):
    Skiped = True

    def getAnimatable(self):
        return self.Object
        pass
    pass