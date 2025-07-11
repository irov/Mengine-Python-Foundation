from Foundation.Task.Task import Task

class TaskPrintFormat(Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskPrintFormat, self)._onParams(params)

        self.Value = params.get("Value")
        self.Args = params.get("Args", ())
        self.Kwargs = params.get("Kwargs", {})
        pass

    def _onValidate(self):
        super(TaskPrintFormat, self)._onValidate()

        if self.Kwargs is None:
            self.validateFailed("TaskPrintFormat Kwargs is None")
            pass

        try:
            str(self.Value).format(*self.Args)
        except Exception as ex:
            self.validateFailed("Invalid TaskPrintFormat format '%s' args '%s'" % (self.Value, self.Args))
            pass
        pass

    def _onRun(self):
        m = str(self.Value).format(*self.Args)

        center = self.Kwargs.get("center", None)

        if center is not None:
            m = m.center(*center)
            pass

        Trace.msg(m)

        return True
        pass
    pass