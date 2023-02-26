from Foundation.Task.Task import Task

class TaskExit(Task):
    Skiped = True

    def _onRun(self):
        Mengine.quitApplication()

        return True
        pass
    pass