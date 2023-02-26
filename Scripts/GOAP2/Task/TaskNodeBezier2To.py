from MixinNode import MixinNode
from Task import Task

class TaskNodeBezier2To(MixinNode, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskNodeBezier2To, self)._onParams(params)

        self.Point1 = params.get("Point1", None)
        self.positionTo = params.get("To")
        self.speed = params.get("Speed", None)
        self.time = params.get("Time", None)
        self.easing = params.get("Easing", "easyLinear")
        self.id = 0

        pass

    def _onInitialize(self):
        super(TaskNodeBezier2To, self)._onInitialize()

        if _DEVELOPMENT is True:
            if self.speed is None and self.time is None:
                self.initializeFailed("Speed and Time is None.")
                pass

            if self.speed == 0:
                self.initializeFailed("Speed is 0.")
                pass
            pass
        pass

    def _onRun(self):
        positionFrom = self.node.getLocalPosition()

        if self.time is None:
            length = Menge.length_v2_v2(positionFrom, self.positionTo)
            self.time = length / self.speed
            pass

        if self.Point1 is None:
            fx = positionFrom[0]
            fy = positionFrom[1]
            tx = self.positionTo[0]
            ty = self.positionTo[1]
            hx = (tx + fx) * 0.5
            hy = (ty + fy) * 0.5

            if ty < fy:
                px = (hx + fx) * 0.5
                py = (hy + ty) * 0.5
            else:
                px = (hx + fx) * 0.5
                py = (hy + ty) * 0.5
                pass

            self.Point1 = (px, py)
            pass

        self.id = self.node.bezier2To(self.time, self.positionTo, self.Point1, self.easing, self._onBezierTo)

        if self.id == 0:
            self.log("[%s] not active" % (self.node.getName()))

            return True
            pass

        return False
        pass

    def _onSkip(self):
        self.id = 0
        self.node.moveStop()
        self.node.setLocalPosition(self.positionTo)
        pass

    def _onBezierTo(self, node, id, isEnd):
        if self.id != id:
            return
            pass

        self.id = 0

        self.complete()
        pass
    pass