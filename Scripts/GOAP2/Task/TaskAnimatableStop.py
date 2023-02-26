from GOAP2.Task.Task import Task

class TaskAnimatableStop(Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskAnimatableStop, self)._onParams(params)
        pass

    def _onRun(self):
        Animatable = self.getAnimation()

        if Animatable is None:
            self.log("Animatable is None")
            return True
            pass

        Animatable.setPlay(False)

        return True
        pass
    pass