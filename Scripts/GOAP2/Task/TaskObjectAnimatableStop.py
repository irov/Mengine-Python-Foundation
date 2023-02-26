from GOAP2.Task.Task import Task

class TaskObjectAnimatableStop(Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskObjectAnimatableStop, self)._onParams(params)
        pass

    def _onRun(self):
        Animatable = self.getAnimatable()

        if Animatable is None:
            return True
            pass

        Animatable.setPlay(False)

        return True
        pass
    pass