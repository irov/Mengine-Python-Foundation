from MixinNode import MixinNode
from Task import Task

class TaskNodeBezier2ScreenFollow(MixinNode, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskNodeBezier2ScreenFollow, self)._onParams(params)

        self.Follow = params.get("Follow")
        self.Time = params.get("Time", None)
        self.Speed = params.get("Speed", None)
        self.Deep = params.get("Deep", 0.0)
        self.Easing = params.get("Easing", "easyLinear")
        self.id = 0
        pass

    def _onCheckParams(self):
        if self.Follow is None:
            self.paramsFailed("Follow is None.")
            pass

        if self.Time is None and self.Speed is None:
            self.paramsFailed("Time and Speed is None.")
            pass
        pass

    def _onInitialize(self):
        super(TaskNodeBezier2ScreenFollow, self)._onInitialize()

        if self.Time is None:
            positionFrom = self.node.getScreenPosition()
            positionTo = self.Follow.getScreenPosition()
            length = Mengine.length_v2_v2(positionFrom, positionTo)
            self.Time = length / self.Speed
            pass
        pass

    def _onRun(self):
        self.id = self.node.bezier2ScreenFollower(self.Time, self.Follow, self.Deep, self.Easing, self._onBezierTo)

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