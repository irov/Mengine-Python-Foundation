from Foundation.ArrowManager import ArrowManager
from Foundation.Task.Task import Task

class TaskMouseMoveDistance(Task):
    def _onParams(self, params):
        super(TaskMouseMoveDistance, self)._onParams(params)

        self.Distance = params.get("Distance")

        self.currentDistance = 0.0
        self.onMouseMoveID = 0
        pass

    def _onRun(self):
        arrow = Mengine.getArrow()
        node = arrow.getNode()
        arrowPosition = node.getLocalPosition()
        self.oldXY = (arrowPosition.x, arrowPosition.y)

        self.onMouseMoveID = Mengine.addMouseMoveHandler(self._onMouseMove)

        return False
        pass

    def _onMouseMove(self, event):
        distance = pow(pow(event.dx, 2.0) + pow(event.dy, 2.0), 0.5)

        self.currentDistance = self.currentDistance + distance
        self.oldXY = (event.dx, event.dy)

        if self.currentDistance < self.Distance:
            return
            pass

        Mengine.removeGlobalHandler(self.onMouseMoveID)

        self.complete()
        return
        pass
    pass