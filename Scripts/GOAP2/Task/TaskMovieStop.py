from GOAP2.Task.MixinObjectTemplate import MixinMovie
from GOAP2.Task.TaskObjectAnimatableStop import TaskObjectAnimatableStop

class TaskMovieStop(MixinMovie, TaskObjectAnimatableStop):
    Skiped = True

    def getAnimatable(self):
        return self.Movie
        pass
    pass