from Foundation.Task.Task import Task

class TaskPrintTrace(Task):
    Skiped = False

    def _onParams(self, params):
        super(TaskPrintTrace, self)._onParams(params)
        pass

    def _onRun(self):
        Trace.trace()

        return True
        pass
    pass