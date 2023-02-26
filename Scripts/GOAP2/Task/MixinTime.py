from GOAP2.Task.Task import Task

class MixinTime(Task):
    __metaclass__ = baseslots("time")

    MixinTime_Validate_TimeZero = True

    def _onParams(self, params):
        super(MixinTime, self)._onParams(params)

        self.time = params.get("Time", 0.0)
        pass

    def _onValidate(self):
        super(MixinTime, self)._onValidate()

        if isinstance(self.time, int) is False and isinstance(self.time, float) is False:
            self.validateFailed("MixinTime time '%s' type '%s' but must number" % (self.time, type(self.time)))
            pass

        if self.time == 0.0 and self.MixinTime_Validate_TimeZero is True:
            self.validateFailed("MixinTime time is not 0.0")
            pass

        if self.time < 0.0:
            self.validateFailed("MixinTime time is less 0.0 [{}]".format(self.time))
            pass
        pass
    pass