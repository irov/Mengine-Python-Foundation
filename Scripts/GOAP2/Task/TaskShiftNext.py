from GOAP2.Task.MixinObjectTemplate import MixinShift
from GOAP2.Task.Task import Task

class TaskShiftNext(MixinShift, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskShiftNext, self)._onParams(params)
        pass

    def _onInitialize(self):
        super(TaskShiftNext, self)._onInitialize()
        pass

    def _onRun(self):
        NextShift = self.Shift.getNextShift()
        self.Shift.setParam("Shift", NextShift)

        return True
        pass
    pass