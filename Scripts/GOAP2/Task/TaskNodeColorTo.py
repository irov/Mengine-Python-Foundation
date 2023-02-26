from MixinNode import MixinNode
from MixinTime import MixinTime
from Task import Task

class TaskNodeColorTo(MixinNode, MixinTime, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskNodeColorTo, self)._onParams(params)

        self.colorTo = params.get("To", (1.0, 1.0, 1.0, 1.0))
        self.easing = params.get("Easing", "easyLinear")

        self.id = None
        pass

    def _onRun(self):
        self.id = self.node.colorTo(self.time, self.colorTo, self.easing, self._onColorTo)

        if self.id == 0:
            self.log("[%s] not active" % (self.node.getName()))

            return True
            pass

        return False
        pass

    def _onSkip(self):
        self.id = None

        self.node.colorStop()
        self.node.setLocalColor(self.colorTo)
        pass

    def _onColorTo(self, node, id, isEnd):
        if self.id != id:
            return
            pass

        self.id = 0

        self.complete()
        pass
    pass