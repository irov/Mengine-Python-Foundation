from Foundation.Task.Task import Task

class TaskQuitApplication(Task):
    Skiped = True

    def _onRun(self):
        Mengine.quitApplication()

        return True
        pass
    pass