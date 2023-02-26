from GOAP2.Task.MixinObjectTemplate import MixinMovie
from GOAP2.Task.TaskObjectAnimatableEnd import TaskObjectAnimatableEnd

class TaskMovieEnd(MixinMovie, TaskObjectAnimatableEnd):
    Skiped = True

    def getAnimatable(self):
        return self.Movie
        pass
    pass