from MixinNode import MixinNode
from Task import Task


class TaskNodeOriginTo(MixinNode, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskNodeOriginTo, self)._onParams(params)

        self.time = params.get("Time", None)
        self.origin = params.get("Origin")
        self.easing = params.get("Easing", "easyLinear")
        self.id = None

    def _onRun(self):
        if self.time is None:
            self.time = 0.0

        self.id = self.node.originTo(self.time, self.origin, self.easing,
                                     self._onOriginTo)

        if self.id is None:
            self.log("[%s] not active" % (self.node.getName()))

            return True

        return False

    def _onSkip(self):
        self.id = 0
        self.node.moveStop()
        self.node.setOrigin(self.origin)
        return

    def _onFastSkip(self):
        self.node.setOrigin(self.origin)
        return True

    def _onOriginTo(self, node, id, isEnd):
        if self.id != id:
            return

        self.id = None

        self.complete()
