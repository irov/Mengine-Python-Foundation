from Foundation.Task.Task import Task

class TaskArrowHide(Task):
    def _onParams(self, params):
        super(TaskArrowHide, self)._onParams(params)
        self.Value = params.get("Value")
        pass

    def _onRun(self):
        arrow = Mengine.getArrow()
        arrow.localHide(self.Value)

        if self.Value is False:
            Mengine.setCursorMode(True)
        elif self.Value is True:
            Mengine.setCursorMode(False)

        return True
        pass
    pass