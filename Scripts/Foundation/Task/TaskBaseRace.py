from Foundation.Task.TaskBase import TaskBase

class TaskBaseRace(TaskBase):
    __metaclass__ = finalslots("NoSkip", "PrevSkip")

    def __init__(self):
        super(TaskBaseRace, self).__init__()

        self.NoSkip = False
        self.PrevSkip = False
        pass

    def setRaceNoSkip(self, NoSkip):
        self.NoSkip = NoSkip
        pass

    def setRacePrevSkip(self, PrevSkip):
        self.PrevSkip = PrevSkip
        pass

    def _checkRun(self):
        if self.PrevSkip is True:
            self._skipPrev()
            pass

        return True
        pass

    def _checkSkip(self):
        if self.PrevSkip is True:
            self._skipPrev()
            pass

        if self.NoSkip is False:
            self._cancelPrev()

            return True
            pass

        skip = TaskBase._checkSkip(self)

        return skip
        pass
    pass