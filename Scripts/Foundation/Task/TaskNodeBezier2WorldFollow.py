from MixinNode import MixinNode
from Task import Task

class TaskNodeBezier2WorldFollow(MixinNode, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskNodeBezier2WorldFollow, self)._onParams(params)

        self.Follow = params.get("Follow")
        self.Time = params.get("Time", None)
        self.Speed = params.get("Speed", None)
        self.Offset = params.get("Offset", (0.0, 0.0, 0.0))
        self.Easing = params.get("Easing", "easyLinear")

        self.affector = None
        pass

    def _onInitialize(self):
        super(TaskNodeBezier2WorldFollow, self)._onInitialize()

        if self.Time is None:
            if self.Speed is None:
                self.initializeFailed("Time and speed is None.")
            positionFrom = self.node.getWorldPosition()
            followPosition = self.Follow.getWorldPosition()
            positionTo = (followPosition[0] + self.Offset[0], followPosition[1] + self.Offset[1])
            point1 = (positionTo[0], positionFrom[1])
            length = Mengine.length_bezier2(positionFrom, point1, positionTo)
            self.Time = length / self.Speed
            pass
        pass

    def _onRun(self):
        def __onBezierTo(node, isEnd):
            self.affector = None

            self.complete(isSkiped=isEnd is False)
            pass

        self.affector = self.node.bezier2WorldFollower(self.Time, self.Follow, self.Offset, self.Easing, __onBezierTo)

        if self.affector is None:
            self.log("[%s] not active" % (self.node.getName()))

            return True

        return False

    def _onSkip(self):
        self.affector = None

        self.node.moveStop()
        return
    pass