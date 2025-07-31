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

        self.affector = None
        pass

    def _onRun(self):
        if self.percentFrom is not None:
            self.node.setPercentVisibility(self.percentFrom)

        def __onPercentVisibilityTo(node, isEnd):
            self.affector = None

            self.complete(isSkiped=isEnd is False)
            pass

        self.affector = self.node.setPercentVisibilityTo(self.time, self.percentTo, self.easing, self.__onPercentVisibilityTo)

        if self.affector is None:
            self.log("[%s] not active" % (self.node.getName()))
            return True

        return False

    def _onSkip(self):
        self.affector = None

        self.node.setPercentVisibilityStop()
        self.node.setPercentVisibility(self.percentTo)
        pass
    pass