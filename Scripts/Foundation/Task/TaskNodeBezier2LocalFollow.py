from MixinNode import MixinNode
from Task import Task

class TaskNodeBezier2LocalFollow(MixinNode, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskNodeBezier2LocalFollow, self)._onParams(params)

        self.Follow = params.get("Follow")
        self.Time = params.get("Time", None)
        self.Speed = params.get("Speed", None)
        self.Offset = params.get("Offset", (0.0, 0.0, 0.0))
        self.Easing = params.get("Easing", "easyLinear")

        self.affector = None
        pass

    def _onInitialize(self):
        super(TaskNodeBezier2LocalFollow, self)._onInitialize()

        if self.Time is None:
            if self.Speed is None:
                self.initializeFailed("Time and speed is None.")
            positionFrom = self.node.getLocalPosition()
            positionTo = self.Follow.getLocalPosition()
            length = Mengine.length_v2_v2(positionFrom, positionTo)
            self.Time = length / self.Speed
            pass
        pass

    def _onRun(self):
        def __onBezierTo(node, isEnd):
            self.affector = None

            self.complete(isSkiped=isEnd is False)
            pass

        self.affector = self.node.bezier2LocalFollower(self.Time, self.Follow, self.Offset, self.Easing, __onBezierTo)

        if self.affector is None:
            self.log("[%s] not active" % (self.node.getName()))

            return True

        return False

    def _onSkip(self):
        self.id = 0
        self.node.moveStop()
        pass
    pass