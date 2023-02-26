from GOAP2.Task.MixinObjectTemplate import MixinMovie2
from GOAP2.Task.Task import Task

class TaskMovie2Rewind(MixinMovie2, Task):
    Skiped = True

    def _onRun(self):
        self.Movie2.setLastFrame(False)

        return True
        pass

    pass