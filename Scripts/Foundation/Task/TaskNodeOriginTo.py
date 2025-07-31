from MixinNode import MixinNode
from Task import Task

class TaskNodeOriginTo(MixinNode, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskNodeOriginTo, self)._onParams(params)

        self.time = params.get("Time", None)
        self.origin = params.get("Origin")
        self.easing = params.get("Easing", "easyLinear")

        self.affector = None
        pass

    def _onRun(self):
        if self.time is None:
            self.time = 0.0

        def __onOriginTo(node, isEnd):
            self.affector = None

            self.complete(isSkiped=isEnd is False)

        self.affector = self.node.originTo(self.time, self.origin, self.easing, __onOriginTo)

        if self.affector is None:
            self.log("[%s] not active" % (self.node.getName()))

            return True

        return False

    def _onSkip(self):
        self.affector = None

        self.node.moveStop()

        self.node.setOrigin(self.origin)
        pass

    def _onFastSkip(self):
        self.node.setOrigin(self.origin)

        return True