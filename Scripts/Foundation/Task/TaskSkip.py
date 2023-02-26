from Task import Task

class TaskSkip(Task):
    Skiped = True

    def _onRun(self):
        if self.base.skiped is True:
            return True
            pass
        else:
            return False
            pass
        pass
    pass