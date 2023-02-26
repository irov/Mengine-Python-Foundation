from MixinNode import MixinNode
from Task import Task

class TaskNodeBezier3To(MixinNode, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskNodeBezier3To, self)._onParams(params)

        self.Point0 = params.get("Point0")
        self.Point1 = params.get("Point1")
        self.positionTo = params.get("To")
        self.speed = params.get("Speed", None)
        self.time = params.get("Time", None)
        self.easing = params.get("Easing", "easyLinear")
        self.id = 0
        pass

    def _onInitialize(self):
        super(TaskNodeBezier3To, self)._onInitialize()

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
            length = Mengine.length_v2_v2(positionFrom, self.positionTo)
            self.time = (length / self.speed) * 1000.0
            pass

        def __onBezierTo(node, id, isEnd):
            if self.id != id:
                return
                pass

            self.id = None

            self.complete()
            pass

        self.id = self.node.bezier3To(self.time, self.positionTo, self.Point0, self.Point1, self.easing, __onBezierTo)

        if self.id == 0:
            self.log("[%s] not active" % (self.node.getName()))

            return True
            pass

        return False
        pass

    def _onSkip(self):
        self.id = None
        self.node.moveStop()
        self.node.setLocalPosition(self.positionTo)
        pass
    pass