from MixinNode import MixinNode
from MixinTime import MixinTime
from Task import Task

class TaskNodePercentVisibilityTo(MixinNode, MixinTime, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskNodePercentVisibilityTo, self)._onParams(params)

        self.percentFrom = params.get("From", None)
        self.percentTo = params.get("To")
        self.easing = params.get("Easing", "easyLinear")

        self.id = None
        pass

    def _onRun(self):
        if self.percentFrom is not None:
            self.node.setPercentVisibility(self.percentFrom)
            pass

        self.id = self.node.setPercentVisibilityTo(self.time, self.percentTo, self.easing, self.__onPercentVisibilityTo)

        if self.id == 0:
            self.log("[%s] not active" % (self.node.getName()))
            return True
            pass

        return False
        pass

    def _onSkip(self):
        self.id = None

        self.node.setPercentVisibilityStop()
        self.node.setPercentVisibility(self.percentTo)
        pass

    def __onPercentVisibilityTo(self, node, id, isEnd):
        if self.id != id:
            return
            pass

        self.id = 0

        self.complete()
        pass
    pass