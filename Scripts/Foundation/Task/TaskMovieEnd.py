from Foundation.Task.MixinObjectTemplate import MixinMovie
from Foundation.Task.TaskObjectAnimatableEnd import TaskObjectAnimatableEnd

class TaskMovieEnd(MixinMovie, TaskObjectAnimatableEnd):
    Skiped = True

    def getAnimatable(self):
        return self.Movie
        pass
    pass