from GOAP2.Task.Task import Task

class TaskSkipFunction(Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskSkipFunction, self)._onParams(params)

        self.Fn = Utils.make_functor(params, "Fn")
        pass

    def _onRun(self):
        return False
        pass

    def _onSkip(self):
        self.Fn()

        return True
        pass
    pass