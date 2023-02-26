from Foundation.Task.Task import Task

class TaskCursorClickEmulate(Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskCursorClickEmulate, self)._onParams(params)
        self.position = params.get("Position")
        self.value = params.get("Value")
        pass

    def _onRun(self):
        Menge.pushMouseButtonEvent(0, self.position, 0, self.value)

        return True
        pass

    pass