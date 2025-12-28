from Foundation.Task.Task import Task

class TaskMouseMove(Task):
    def _onParams(self, params):
        super(TaskMouseMove, self)._onParams(params)

        self.Tracker = Utils.make_functor(params, "Tracker")
        pass

    def _onRun(self):
        super(TaskMouseMove, self)._onRun()

        self.onMouseMoveID = Mengine.addMouseMoveHandler(self._onMouseMove)

        return False
        pass

    def _onMouseMove(self, event):
        if self.Tracker(event.touchId, event.position.world.x, event.position.world.y, event.worldDelta.x, event.worldDelta.y) is False:
            return

        self.complete()
        pass

    def _onFinally(self):
        super(TaskMouseMove, self)._onFinally()

        Mengine.removeGlobalHandler(self.onMouseMoveID)
        pass
    pass