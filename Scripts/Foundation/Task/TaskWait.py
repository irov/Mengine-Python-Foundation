from MixinTime import MixinTime
from Task import Task

class TaskWait(MixinTime, Task):
    Skiped = False

    def _onParams(self, params):
        super(TaskWait, self)._onParams(params)

        self.Timing = params.get("Timing", None)

        self.Condition = Utils.make_functor(params, "Condition")

        self.id = 0
        pass

    def _onCheck(self):
        if self.Condition() is False:
            return True
            pass

        return False
        pass

    def _onRun(self):
        if self.Timing is not None:
            self.id = self.Timing.timing(self.time, self.__onTiming)
        else:
            self.id = Mengine.timing(self.time, self.__onTiming)
            pass

        if self.id == 0:
            self.invalidTask("Mengine.schedule return 0 (%f)" % (self.time))

            return True
            pass

        return False
        pass

    def __onTiming(self, id, time, isRemoved):
        if self.id != id:
            return
            pass

        if self.Condition() is False:
            return
            pass

        self.complete()
        pass

    def _onSkip(self):
        remove_id = self.id
        self.id = 0

        if self.Scheduler is not None:
            if self.Timing.remove(remove_id) is False:
                Trace.trace()
                pass
        else:
            if Mengine.timingRemove(remove_id) is False:
                Trace.trace()
                pass
            pass
        pass
    pass