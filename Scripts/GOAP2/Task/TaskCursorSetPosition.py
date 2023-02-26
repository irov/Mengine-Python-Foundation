from GOAP2.Task.Task import Task

class TaskCursorSetPosition(Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskCursorSetPosition, self)._onParams(params)
        self.position = params.get("Position")
        pass

    def _onRun(self):
        Menge.pushMouseMove(0, self.position)
        return True
        pass

    pass