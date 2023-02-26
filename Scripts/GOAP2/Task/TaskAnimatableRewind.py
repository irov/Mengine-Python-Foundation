from GOAP2.Task.Task import Task

class TaskAnimatableRewind(Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskAnimatableRewind, self)._onParams(params)

        self.Animatable = params.get("Animatable")
        self.AutoEnable = params.get("AutoEnable", False)
        pass

    def _onValidate(self):
        super(TaskAnimatableRewind, self)._onValidate()

        if Menge.isHomeless(self.Animatable) is True:
            self.validateFailed("Animatable %s is Homeless" % (self.Animatable.getName()))
            pass

        Enable = self.Animatable.isEnable()

        if Enable is False and self.AutoEnable is False:
            self.validateFailed("Animatable %s is Disable" % (self.Animatable.getName()))
            pass
        pass

    def _onRun(self):
        self.Animatable.setFirstFrame()

        return True
        pass
    pass