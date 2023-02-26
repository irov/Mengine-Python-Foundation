from Foundation.Task.MixinObjectTemplate import MixinMovie
from Foundation.Task.TaskObjectAnimatablePlay import TaskObjectAnimatablePlay

class TaskMoviePlay(MixinMovie, TaskObjectAnimatablePlay):
    Skiped = True

    def getAnimatable(self):
        return self.Movie
        pass
    pass