from Foundation.Task.Task import Task

class TaskSetCapture(Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskSetCapture, self)._onParams(params)

        self.Capture = params.get("Capture")
        self.Type = params.get("Type", None)
        self.Args = params.get("Args", ())
        self.Kwargs = params.get("Kwargs", {})
        pass

    def _onRun(self):
        self.Capture.setValue(self.Type, *self.Args, **self.Kwargs)

        return True
        pass
    pass