from Foundation.Task.Task import Task

class TaskFunction(Task):
    __metaclass__ = finalslots("Fn")

    Skiped = True

    def _onParams(self, params):
        super(TaskFunction, self)._onParams(params)

        self.Fn = Utils.make_functor(params, "Fn")
        pass

    def _onValidate(self, params):
        super(TaskFunction, self)._onValidate(params)

        if Utils.is_valid_functor(self.Fn) is False:
            self.validateFailed(params, "Fn %s is not callable" % (self.Fn))
            pass
        pass

    def _onRun(self):
        self.Fn()

        return True
    pass