from Task import Task

class TaskDeadLock(Task):
    def _onRun(self):
        return False
        pass
    pass