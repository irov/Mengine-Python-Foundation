from Foundation.Task.Task import Task

class TaskSetWrapper(Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskSetWrapper, self)._onParams(params)

        self.Wrapper = params.get("Wrapper")
        self.Value = params.get("Value")
        pass

    def _onRun(self):
        self.Wrapper.setValue(self.Value)

        return True
        pass
    pass