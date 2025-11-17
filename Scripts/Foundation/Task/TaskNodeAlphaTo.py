from MixinNode import MixinNode
from MixinTime import MixinTime
from Task import Task

class TaskNodeAlphaTo(MixinNode, MixinTime, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskNodeAlphaTo, self)._onParams(params)

        self.alphaFrom = params.get("From", None)
        self.alphaTo = params.get("To")
        self.interrupt = params.get("Interrupt", False)
        self.easing = params.get("Easing", "easyLinear")

        self.isTemp = params.get("IsTemp", False)
        self.alphaOrig = 1.0

        self.affector = None

    def _onRun(self):
        render = self.node.getRender()

        if render is not None:
            if self.isTemp:
                self.alphaOrig = render.getLocalAlpha()

            if self.alphaFrom is not None:
                render.setLocalAlpha(self.alphaFrom)

        if self.node.isActivate() is False:
            self.log("[%s] not active - alphaTo not started" % (self.node.getName()))
            return True

        def __onAlphaTo(node, isEnd):
            self.affector = None

            self.complete(isSkiped=isEnd is False)
            pass

        self.affector = self.node.alphaTo(self.time, self.alphaTo, self.easing, __onAlphaTo)

        if self.affector is None:
            self.log("[%s] not active - affectorId==0" % (self.node.getName()))
            return True

        return False

    def _onFastSkip(self):
        render = self.node.getRender()
        if render is not None:
            if self.isTemp:
                render.setLocalAlpha(self.alphaOrig)
            else:
                render.setLocalAlpha(self.alphaTo)

        return True

    def _onSkip(self):
        self.affector = None

        self.node.colorStop()

        if self.isTemp:
            render = self.node.getRender()

            if render is not None:
                render.setLocalAlpha(self.alphaOrig)
                pass
        elif self.interrupt is False:
            render = self.node.getRender()

            if render is not None:
                render.setLocalAlpha(self.alphaTo)
                pass
            pass
        pass

    def _onComplete(self):
        if self.isTemp:
            render = self.node.getRender()

            if render is not None:
                render.setLocalAlpha(self.alphaOrig)
                pass
            pass
        pass