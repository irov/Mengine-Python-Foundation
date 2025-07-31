from MixinNode import MixinNode
from MixinTime import MixinTime
from Task import Task

class TaskNodeScaleTo(MixinNode, MixinTime, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskNodeScaleTo, self)._onParams(params)

        self.scaleFrom = params.get("From", None)
        self.scaleTo = params.get("To")
        self.easing = params.get("Easing", "easyLinear")

        self.affector = None
        pass

    def _onRun(self):
        if self.scaleFrom is not None:
            self.node.setScale(self.scaleFrom)
            pass

        def __onScaleTo(node, isEnd):
            self.affector = None

            self.complete(isSkiped=isEnd is False)
            pass

        self.affector = self.node.scaleTo(self.time, self.scaleTo, self.easing, __onScaleTo)

        if self.affector is None:
            self.log("[%s] not active" % (self.node.getName()))
            return True

        return False

    def _onFastSkip(self):
        self.node.setScale(self.scaleTo)

        return True

    def _onSkip(self):
        self.affector = None

        self.node.scaleStop()
        self.node.setScale(self.scaleTo)
        pass
    pass