from GOAP2.Task.Task import Task

class TaskSemaphoreIncrement(Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskSemaphoreIncrement, self)._onParams(params)

        self.Semaphore = params.get("Semaphore")
        self.Inc = params.get("Increment")

    def _onValidate(self):
        super(TaskSemaphoreIncrement, self)._onValidate()

        if self.Inc is None:
            self.validateFailed("Semaphore '%s' setup Increment" % (self.Semaphore))

        if not isinstance(self.Inc, int):
            self.validateFailed("Semaphore '%s' Increment must be an integer" % (self.Semaphore))

        if isinstance(self.Semaphore, Semaphore) is False:
            self.validateFailed("Semaphore '%s' is not Semaphore type" % (self.Semaphore))

    def _onRun(self):
        SemaphoreValue = self.Semaphore.getValue()

        self.Semaphore.setValue(SemaphoreValue + self.Inc)

        return True