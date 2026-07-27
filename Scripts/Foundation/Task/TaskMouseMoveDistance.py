from Foundation.Task.Task import Task

class TaskMouseMoveDistance(Task):
    def _onParams(self, params):
        super(TaskMouseMoveDistance, self)._onParams(params)

        self.Distance = params.get("Distance")
        self.Button = params.get("Button", 0)

        self.startX = 0.0
        self.startY = 0.0
        self.onMouseMoveID = 0
        pass

    def _onRun(self):
        arrowPosition = Mengine.getArrowNode().getLocalPosition()
        self.startX = arrowPosition.x
        self.startY = arrowPosition.y

        self.onMouseMoveID = Mengine.addMouseMoveHandler(self._onMouseMove)

        return False
        pass

    def _onMouseMove(self, event):
        if Mengine.isMouseButtonDown(self.Button) is False:
            return

        arrowPosition = Mengine.getArrowNode().getLocalPosition()
        deltaX = arrowPosition.x - self.startX
        deltaY = arrowPosition.y - self.startY

        distance = pow(pow(deltaX, 2.0) + pow(deltaY, 2.0), 0.5)

        if distance < self.Distance:
            return
            pass

        Mengine.removeGlobalHandler(self.onMouseMoveID)
        self.onMouseMoveID = 0

        self.complete()
        return
        pass

    def _onFinally(self):
        super(TaskMouseMoveDistance, self)._onFinally()

        if self.onMouseMoveID != 0:
            Mengine.removeGlobalHandler(self.onMouseMoveID)
            self.onMouseMoveID = 0
            pass
        pass
    pass
