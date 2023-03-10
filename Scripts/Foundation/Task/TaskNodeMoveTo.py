from MixinNode import MixinNode
from MixinTime import MixinTime
from Task import Task

class TaskNodeMoveTo(MixinNode, MixinTime, Task):
    Skiped = True
    MixinTime_Validate_TimeZero = False

    def _onParams(self, params):
        super(TaskNodeMoveTo, self)._onParams(params)

        self.positionFrom = params.get("From", None)
        self.positionTo = params.get("To")
        self.speed = params.get("Speed", None)
        self.interrupt = params.get("Interrupt", False)
        self.easing = params.get("Easing", "easyLinear")

        self.id = None
        pass

    def _onInitialize(self):
        super(TaskNodeMoveTo, self)._onInitialize()

        if _DEVELOPMENT is True:
            if self.positionTo is None:
                self.initializeFailed("PositionTo not initialized")
                pass
            pass
        pass

    def _onRun(self):
        if self.positionFrom is not None:
            self.node.setLocalPosition(self.positionFrom)
            pass

        positionFrom = self.node.getLocalPosition()

        if self.speed is not None:
            length = Mengine.length_v2_v2(positionFrom, self.positionTo)
            self.time = (length / self.speed) * 1000.0
            pass

        def __onMoveTo(node, id, isEnd):
            if self.id != id:
                return
                pass

            self.id = None

            self.complete(isSkiped=isEnd is False)
            pass

        self.id = self.node.moveTo(self.time, self.positionTo, self.easing, __onMoveTo)

        if self.id == 0:
            self.log("[%s] not active" % (self.node.getName()))

            return True
            pass

        return False
        pass

    def _onSkip(self):
        self.id = None

        self.node.moveStop()

        if self.interrupt is False:
            self.node.setLocalPosition(self.positionTo)
            pass
        pass
    pass