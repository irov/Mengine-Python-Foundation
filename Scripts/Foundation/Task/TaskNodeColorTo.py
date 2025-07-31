from MixinNode import MixinNode
from MixinTime import MixinTime
from Task import Task

class TaskNodeColorTo(MixinNode, MixinTime, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskNodeColorTo, self)._onParams(params)

        self.colorTo = params.get("To", (1.0, 1.0, 1.0, 1.0))
        self.easing = params.get("Easing", "easyLinear")

        self.affector = None
        pass

    def _onRun(self):
        def __onColorTo(node, isEnd):
            self.affector = None

            self.complete(isSkiped=isEnd is False)
            pass

        self.affector = self.node.colorTo(self.time, self.colorTo, self.easing, __onColorTo)

        if self.affector is None:
            self.log("[%s] not active" % (self.node.getName()))

            return True

        return False

    def _onSkip(self):
        self.affector = None

        self.node.colorStop()
        self.node.setLocalColor(self.colorTo)
        pass
    pass