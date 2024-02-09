from Foundation.Task.Task import Task


class TaskObjectAnimatableResume(Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskObjectAnimatableResume, self)._onParams(params)

    def _onRun(self):
        Animatable = self.getAnimatable()

        if Animatable is None:
            self.log("Animatable is None")
            return True

        Animatable.setPause(False)

        return True
