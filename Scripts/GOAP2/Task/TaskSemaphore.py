from GOAP2.Task.MixinEvent import MixinEvent
from GOAP2.Task.Task import Task

class TaskSemaphore(MixinEvent, Task):
    __metaclass__ = finalslots("Semaphore", "From", "Less", "To", "Change", "Skiped")

    def _onParams(self, params):
        super(TaskSemaphore, self)._onParams(params)

        self.Semaphore = params.get("Semaphore")
        self.From = params.get("From")
        self.Less = params.get("Less")
        self.To = params.get("To")
        self.Change = params.get("Change", False)

        if self.Less is None and self.Change is False:
            if self.From is None:
                self.Skiped = True
                pass
            elif self.From == self.Semaphore.getValue():
                self.Skiped = True
                pass
            else:
                self.Skiped = False
                pass
            pass
        else:
            self.Skiped = False
            pass
        pass

    def _onValidate(self):
        super(TaskSemaphore, self)._onValidate()

        if self.From is not None and self.Less is not None:
            self.validateFailed("Semaphore '%s' choose one of [From, Less]" % (self.Semaphore))
            pass

        if isinstance(self.Semaphore, Semaphore) is False:
            self.validateFailed("Semaphore '%s' is not Semaphore type" % (self.Semaphore))
            pass
        pass

    def _onCheck(self):
        if self.Change is True:
            return True
            pass

        if self.From is not None:
            Value = self.Semaphore.getValue()

            if self.From != Value:
                return True
                pass
            pass
        elif self.Less is not None:
            Value = self.Semaphore.getValue()

            if self.Less <= Value:
                return True
                pass
            pass

        if self.To is not None:
            self.Semaphore.setValue(self.To)
            pass

        return False
        pass

    def _onRun(self):
        def __testSemaphore():
            if self.Change is True:
                return True
                pass

            SemaphoreValue = self.Semaphore.getValue()

            if self.From is not None:
                return self.From == SemaphoreValue
                pass
            elif self.Less is not None:
                return self.Less > SemaphoreValue
                pass
            pass

        Event = self.Semaphore.getEvent()

        self.addEvent(Event, __testSemaphore)

        return False
        pass

    def _onComplete(self):
        if self.To is not None:
            self.Semaphore.setValue(self.To)
            pass
        pass
    pass