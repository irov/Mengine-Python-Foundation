from Foundation.Task.Task import Task

class TaskMouseMove(Task):
    def _onParams(self, params):
        super(TaskMouseMove, self)._onParams(params)

        self.Tracker = Utils.make_functor(params, "Tracker")
        pass

    def _onRun(self):
        super(TaskMouseMove, self)._onRun()

        self.onMouseMoveID = Menge.addMouseMoveHandler(self._onMouseMove)

        return False
        pass

    def _onMouseMove(self, event):
        if self.Tracker(event.touchId, event.x, event.y, event.dx, event.dy) is False:
            return
            pass

        self.complete()
        pass

    def _onFinally(self):
        super(TaskMouseMove, self)._onFinally()

        Menge.removeGlobalHandler(self.onMouseMoveID)
        pass
    pass