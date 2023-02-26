from GOAP2.Task.MixinObjectTemplate import MixinMovie
from GOAP2.Task.TaskObjectAnimatablePlay import TaskObjectAnimatablePlay

class TaskMoviePlay(MixinMovie, TaskObjectAnimatablePlay):
    Skiped = True

    def getAnimatable(self):
        return self.Movie
        pass
    pass