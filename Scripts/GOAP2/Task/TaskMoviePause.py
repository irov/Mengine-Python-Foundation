from GOAP2.Task.MixinObjectTemplate import MixinMovie
from GOAP2.Task.TaskObjectAnimatablePause import TaskObjectAnimatablePause

class TaskMoviePause(MixinMovie, TaskObjectAnimatablePause):
    Skiped = True

    def getAnimatable(self):
        return self.Movie
        pass
    pass