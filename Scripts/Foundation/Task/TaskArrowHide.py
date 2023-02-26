from Foundation.Task.Task import Task

class TaskArrowHide(Task):
    def _onParams(self, params):
        super(TaskArrowHide, self)._onParams(params)
        self.Value = params.get("Value")
        pass

    def _onRun(self):
        arrow = Menge.getArrow()
        arrow.localHide(self.Value)

        if self.Value is False:
            Menge.setCursorMode(True)
        elif self.Value is True:
            Menge.setCursorMode(False)

        return True
        pass
    pass