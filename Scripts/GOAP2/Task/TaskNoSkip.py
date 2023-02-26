from Task import Task

class TaskNoSkip(Task):
    __metaclass__ = finalslots("id")

    Skiped = False
    SkipBlock = True

    def __init__(self):
        super(TaskNoSkip, self).__init__()

        self.id = 0
        pass

    def _onRun(self):
        return True
        pass

    def _onSkipBlock(self):
        self.id = Menge.schedule(0.0, self._onDelay)

        return False
        pass

    def _onDelay(self, id, isRemoved):
        if self.id != id:
            return
            pass

        self.id = 0

        self.complete()
        pass

    def _onCancel(self):
        if self.id == 0:
            return
            pass

        id = self.id
        self.id = 0
        Menge.scheduleRemove(id)
        pass
    pass