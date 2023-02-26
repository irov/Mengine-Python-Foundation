from Foundation.Task.MixinObjectTemplate import MixinMovie
from Foundation.Task.TaskObjectAnimatableStop import TaskObjectAnimatableStop

class TaskMovieStop(MixinMovie, TaskObjectAnimatableStop):
    Skiped = True

    def getAnimatable(self):
        return self.Movie
        pass
    pass