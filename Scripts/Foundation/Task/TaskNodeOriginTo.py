from MixinNode import MixinNode
from Task import Task

class TaskNodeOriginTo(MixinNode, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskNodeOriginTo, self)._onParams(params)

        self.time = params.get("Time", None)
        self.origin = params.get("Origin")
        self.easing = params.get("Easing", "easyLinear")
        self.id = 0
        pass

    def _onRun(self):
        self.id = self.node.originTo(self.time, self.origin, self.easing, self._onOriginTo)

        if self.id == 0:
            self.log("[%s] not active" % (self.node.getName()))

            return True
            pass

        return False
        pass

    def _onSkip(self):
        self.id = 0
        self.node.moveStop()
        return

    def _onOriginTo(self, node, id, isEnd):
        if self.id != id:
            return
            pass

        self.id = 0

        self.complete()
        pass
    pass