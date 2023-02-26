from Foundation.Task.Task import Task

class TaskCallback(Task):
    __metaclass__ = finalslots("Cb")

    Skiped = True

    def _onParams(self, params):
        super(TaskCallback, self)._onParams(params)

        self.Cb = Utils.make_functor(params, "Cb")
        pass

    def _onValidate(self):
        super(TaskCallback, self)._onValidate()

        if Utils.is_valid_functor_args(self.Cb, 2) is False:
            self.validateFailed("Cb %s is bad arguments or kwds" % (self.Cb))
            pass
        pass

    def _onRun(self):
        isSkip = self.isSkiped()

        self.Cb(isSkip, self.__onCallbackFilter)

        return False
        pass

    def __onCallbackFilter(self, isSkip):
        if isSkip is False:
            self.complete()
            pass
        pass
    pass