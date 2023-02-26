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

        self.id = None
        pass

    def _onRun(self):
        if self.scaleFrom is not None:
            self.node.setScale(self.scaleFrom)
            pass

        self.id = self.node.scaleTo(self.time, self.scaleTo, self.easing, self._onScaleTo)

        if self.id == 0:
            self.log("[%s] not active" % (self.node.getName()))
            return True
            pass

        return False
        pass

    def _onFastSkip(self):
        self.node.setScale(self.scaleTo)

        return True
        pass

    def _onSkip(self):
        self.id = None

        self.node.scaleStop()
        self.node.setScale(self.scaleTo)
        pass

    def _onScaleTo(self, node, id, isEnd):
        if self.id != id:
            return
            pass

        self.id = 0

        self.complete(isSkiped=isEnd is False)
        pass
    pass