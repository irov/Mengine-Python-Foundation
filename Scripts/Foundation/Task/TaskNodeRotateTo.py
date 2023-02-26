from MixinNode import MixinNode
from MixinTime import MixinTime
from Task import Task

class TaskNodeRotateTo(MixinNode, MixinTime, Task):
    Skiped = True
    MixinTime_Validate_TimeZero = False

    def _onParams(self, params):
        super(TaskNodeRotateTo, self)._onParams(params)

        self.rotateTo = params.get("To")
        self.easing = params.get("Easing", "easyLinear")
        self.additive = params.get("Additive", False)

        self.id = None
        pass

    def _onInitialize(self):
        super(TaskNodeRotateTo, self)._onInitialize()

        if self.additive:
            self.rotateTo += self.node.getAngle()

        # self.rotateTo *= 3.14159 / 180.0
        pass

    def _onRun(self):
        self.id = self.node.angleTo(self.time, self.rotateTo, self.easing, self._onRotateTo)

        if self.id == 0:
            self.log("[%s] not active" % (self.node.getName()))
            return True
            pass

        return False
        pass

    def _onFastSkip(self):
        self.node.setAngle(self.rotateTo)

        return True
        pass

    def _onSkip(self):
        self.id = None

        self.node.angleStop()
        self.node.setAngle(self.rotateTo)
        pass

    def _onRotateTo(self, node, id, isEnd):
        if self.id != id:
            return
            pass

        self.id = 0

        self.complete()
        pass
    pass