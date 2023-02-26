from GOAP2.Task.Task import Task

class TaskAnimatablePause(Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskAnimatablePause, self)._onParams(params)
        pass

    def _onRun(self):
        Animatable = self.getAnimation()

        if Animatable is None:
            self.log("Animatable is None")
            return True
            pass

        Animatable.setPause(True)

        return True
        pass
    pass