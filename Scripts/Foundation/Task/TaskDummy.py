from Task import Task

class TaskDummy(Task):
    __metaclass__ = finalslots()

    Skiped = True

    def _onRun(self):
        return True
        pass
    pass