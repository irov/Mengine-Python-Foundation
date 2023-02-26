from MixinNode import MixinNode
from Task import Task

class TaskNodeParabolaTo(MixinNode, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskNodeParabolaTo, self)._onParams(params)

        self.Height = params.get("Height")
        self.positionTo = params.get("To")
        self.speed = params.get("Speed", None)
        self.time = params.get("Time", None)
        self.easing = params.get("Easing", "easyLinear")
        self.id = 0
        pass

    def _onInitialize(self):
        super(TaskNodeParabolaTo, self)._onInitialize()

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
            length = Menge.length_v3_v3(positionFrom, self.positionTo)
            self.time = (length / self.speed) * 1000.0
            pass

        def __onParabolaTo(node, id, isEnd):
            if self.id != id:
                return
                pass

            self.id = None

            self.complete()
            pass

        self.id = self.node.parabolaTo(self.time, self.positionTo, self.Height, self.easing, __onParabolaTo)

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