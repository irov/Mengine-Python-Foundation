from Foundation.Task.MixinObjectTemplate import MixinMovie

from Foundation.Task.TaskObjectAnimatableInterrupt import TaskObjectAnimatableInterrupt

class TaskMovieInterrupt(MixinMovie, TaskObjectAnimatableInterrupt):
    Skiped = True

    def getAnimatable(self):
        return self.Movie
        pass
    pass