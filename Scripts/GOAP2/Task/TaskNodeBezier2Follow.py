from MixinNode import MixinNode
from Task import Task

class TaskNodeBezier2Follow(MixinNode, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskNodeBezier2Follow, self)._onParams(params)

        self.Follow = params.get("Follow")
        self.Time = params.get("Time", None)
        self.speed = params.get("Speed", None)
        self.Offset = params.get("Offset", (0.0, 0.0))
        self.easing = params.get("Easing", "easyLinear")
        self.id = 0
        pass

    def _onInitialize(self):
        super(TaskNodeBezier2Follow, self)._onInitialize()

        if self.Time is None:
            if self.speed is None:
                self.initializeFailed("Time and speed is None.")
            positionFrom = self.node.getWorldPosition()
            positionTo = self.Follow.getWorldPosition()
            length = Menge.length_v2_v2(positionFrom, positionTo)
            self.Time = length / self.speed
            pass
        pass

    def _onRun(self):
        self.id = self.node.bezier2Follower(self.Time, self.Follow, self.Offset, self.easing, self._onBezierTo)

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