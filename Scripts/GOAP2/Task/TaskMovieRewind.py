from GOAP2.Task.MixinObjectTemplate import MixinMovie
from GOAP2.Task.Task import Task

class TaskMovieRewind(MixinMovie, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskMovieRewind, self)._onParams(params)
        pass

    def _onRun(self):
        self.Movie.setLastFrame(False)

        return True
        pass

    pass