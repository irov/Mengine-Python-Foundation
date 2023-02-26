from Foundation.Task.MixinObjectTemplate import MixinMovie
from Foundation.Task.TaskObjectAnimatablePause import TaskObjectAnimatablePause

class TaskMoviePause(MixinMovie, TaskObjectAnimatablePause):
    Skiped = True

    def getAnimatable(self):
        return self.Movie
        pass
    pass