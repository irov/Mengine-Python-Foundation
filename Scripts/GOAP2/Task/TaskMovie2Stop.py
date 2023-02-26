from GOAP2.Task.MixinObjectTemplate import MixinMovie2
from GOAP2.Task.TaskObjectAnimatableStop import TaskObjectAnimatableStop

class TaskMovie2Stop(MixinMovie2, TaskObjectAnimatableStop):
    Skiped = True

    def getAnimatable(self):
        return self.Movie2
        pass
    pass