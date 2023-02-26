from Foundation.Task.Task import Task

class TaskDebugBreak(Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskDebugBreak, self)._onParams(params)

        self.Value = params.get("Value")
        pass

    def _onRun(self):
        # self.invalidTask("break: %s"%(self.Value))
        Menge.debug()

        return True
        pass
    pass