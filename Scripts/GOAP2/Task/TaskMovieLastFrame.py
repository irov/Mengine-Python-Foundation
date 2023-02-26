from GOAP2.Task.MixinObjectTemplate import MixinMovie
from GOAP2.Task.Task import Task

class TaskMovieLastFrame(MixinMovie, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskMovieLastFrame, self)._onParams(params)

        self.Value = params.get("Value")
        pass

    def _onRun(self):
        self.Movie.setLastFrame(self.Value)

        return True
        pass

    pass