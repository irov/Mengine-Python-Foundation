from GOAP2.Task.MixinObjectTemplate import MixinMovie

from GOAP2.Task.TaskObjectAnimatableInterrupt import TaskObjectAnimatableInterrupt

class TaskMovieInterrupt(MixinMovie, TaskObjectAnimatableInterrupt):
    Skiped = True

    def getAnimatable(self):
        return self.Movie
        pass
    pass