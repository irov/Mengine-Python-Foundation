from GOAP2.Task.Task import Task

class TaskPrint(Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskPrint, self)._onParams(params)

        self.Value = params.get("Value")
        self.Args = params.get("Args", ())
        pass

    def _onValidate(self):
        try:
            str(self.Value) % self.Args
        except TypeError as ex:
            self.validateFailed("Invalid TaskPrint format '%s' args '%s'" % (self.Value, self.Args))
            pass
        pass

    def _onRun(self):
        Trace.msg(str(self.Value) % self.Args)

        return True
        pass
    pass