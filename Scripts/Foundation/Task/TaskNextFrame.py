from Foundation.Task.Task import Task

class TaskNextFrame(Task):
    Skiped = True

    def __init__(self):
        super(TaskNextFrame, self).__init__()

        self.CallbackId = 0
        pass

    def _onFastSkip(self):
        return True

    def _onRun(self):
        self.CallbackId = Mengine.addTimebeginCallback(self.__onNextFrame)

        return False

    def __onNextFrame(self):
        self.CallbackId = 0
        self.complete()
        pass

    def _onFinally(self):
        if self.CallbackId != 0:
            Mengine.removeTimebeginCallback(self.CallbackId)
            self.CallbackId = 0
            pass
        pass
    pass
