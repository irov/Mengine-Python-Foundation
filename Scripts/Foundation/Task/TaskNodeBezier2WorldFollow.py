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
        self.id = 0
        pass

    def _onInitialize(self):
        super(TaskNodeBezier2WorldFollow, self)._onInitialize()

        if self.Time is None:
            if self.Speed is None:
                self.initializeFailed("Time and speed is None.")
            positionFrom = self.node.getWorldPosition()
            positionTo = self.Follow.getWorldPosition()
            length = Mengine.length_v2_v2(positionFrom, positionTo)
            self.Time = length / self.Speed
            pass
        pass

    def _onRun(self):
        self.id = self.node.bezier2WorldFollower(self.Time, self.Follow, self.Offset, self.Easing, self._onBezierTo)

        if self.id == 0:
            self.log("[%s] not active" % (self.node.getName()))

            return True
            pass

        return False
        pass

    def _onSkip(self):
        self.id = 0
        self.node.moveStop()
        return

    def _onBezierTo(self, node, id, isEnd):
        if self.id != id:
            return
            pass

        self.id = 0

        self.complete()
        pass
    pass