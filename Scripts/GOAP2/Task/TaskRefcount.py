from GOAP2.Task.MixinEvent import MixinEvent
from GOAP2.Task.Task import Task

class TaskRefcount(MixinEvent, Task):
    __metaclass__ = finalslots("Refcount", "Increase", "Skiped")

    def _onParams(self, params):
        super(TaskRefcount, self)._onParams(params)

        self.Refcount = params.get("Refcount")
        self.Increase = params.get("Increase")

        if self.Increase is not None:
            self.Skiped = True
            pass
        else:
            self.Skiped = False
            pass
        pass

    def _onValidate(self):
        super(TaskRefcount, self)._onValidate()

        if isinstance(self.Refcount, Refcount) is False:
            self.validateFailed("Refcount '%s' is not Refcount type" % (self.Refcount))
            pass
        pass

    def _onCheck(self):
        if self.Increase is None:
            if self.Refcount.isKeep() is True:
                return True
                pass
            else:
                return False
                pass
            pass
        else:
            if self.Increase is True:
                self.Refcount.incref()
                pass
            else:
                self.Refcount.decref()
                pass
            pass

        return False
        pass

    def _onRun(self):
        def __testRefcount(keep):
            return keep is False
            pass

        Event = self.Refcount.getEvent()

        self.addEvent(Event, __testRefcount)

        return False
        pass
    pass