from Foundation.Task.Task import Task

class TaskPrintFormat(Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskPrintFormat, self)._onParams(params)

        self.Value = params.get("Value")
        self.Args = params.get("Args", ())

        self.center = params.get("center", None)
        pass

    def _onValidate(self, params):
        super(TaskPrintFormat, self)._onValidate(params)

        try:
            str(self.Value).format(*self.Args)
        except Exception as ex:
            self.validateFailed(params, "Invalid TaskPrintFormat format '%s' args '%s' exception '%s'" % (self.Value, self.Args, ex))
            pass
        pass

    def _onRun(self):
        m = str(self.Value).format(*self.Args)

        if self.center is not None:
            m = m.center(*self.center)
            pass

        Trace.msg(m)

        return True
    pass