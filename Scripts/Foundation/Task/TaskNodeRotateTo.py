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

        self.affector = None
        pass

    def _onInitialize(self):
        super(TaskNodeRotateTo, self)._onInitialize()

        if self.additive:
            self.rotateTo += self.node.getAngle()

        # self.rotateTo *= 3.14159 / 180.0
        pass

    def _onRun(self):
        def __onRotateTo(node, isEnd):
            self.affector = None

            self.complete(isSkiped=isEnd is False)
            pass

        self.affector = self.node.angleTo(self.time, self.rotateTo, self.easing, __onRotateTo)

        if self.affector is None:
            self.log("[%s] not active" % (self.node.getName()))
            return True

        return False

    def _onFastSkip(self):
        self.node.setAngle(self.rotateTo)

        return True

    def _onSkip(self):
        self.affector = None

        self.node.angleStop()
        self.node.setAngle(self.rotateTo)
        pass
    pass