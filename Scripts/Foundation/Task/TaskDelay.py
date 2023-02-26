from MixinTime import MixinTime
from Task import Task

class TaskDelay(MixinTime, Task):
    __metaclass__ = finalslots("Scheduler", "Feedback", "id")

    Skiped = True

    MixinTime_Validate_TimeZero = False

    def __init__(self):
        super(TaskDelay, self).__init__()

        self.Scheduler = None
        self.Feedback = None

        self.id = None
        pass

    def _onParams(self, params):
        super(TaskDelay, self)._onParams(params)

        self.Scheduler = params.get("Scheduler", None)
        self.Feedback = params.get("Feedback", None)
        pass

    def _onFastSkip(self):
        return True
        pass

    def _onRun(self):
        if self.Scheduler is not None:
            self.id = self.Scheduler.schedule(self.time, self.__onDelay)
        else:
            self.id = Mengine.schedule(self.time, self.__onDelay)
            pass

        if self.id == 0:
            self.invalidTask("scheduler return 0 (%f)" % (self.time))
            pass

        if self.Feedback is not None:
            self.Feedback.set(self.id)
            pass

        return False
        pass

    def __onDelay(self, id, isRemoved):
        if self.id != id:
            return
            pass

        self.complete()
        pass

    def _onSkip(self):
        remove_id = self.id
        self.id = None

        if self.Scheduler is not None:
            if self.Scheduler.remove(remove_id) is False:
                Trace.trace()
                pass
            pass
        else:
            if Mengine.scheduleRemove(remove_id) is False:
                Trace.trace()
                pass
            pass
        pass
    pass