from MixinNode import MixinNode
from MixinTime import MixinTime
from Task import Task

class TaskNodeAlphaTo(MixinNode, MixinTime, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskNodeAlphaTo, self)._onParams(params)

        self.alphaFrom = params.get("From", None)  # if not None, set current alpha this value, then run alpha to
        self.alphaTo = params.get("To")
        self.interrupt = params.get("Interrupt", False)  # if true set alphaTo on task interrupt
        self.easing = params.get("Easing", "easyLinear")

        self.isTemp = params.get("IsTemp", False)  # restore node original render local alpha when task complete/skipped
        self.alphaOrig = 1.0  # original node alpha value

        self.affectorId = None

    def _onRun(self):
        render = self.node.getRender()

        if render is not None:
            if self.isTemp:  # if isTemp get original alpha
                self.alphaOrig = render.getLocalAlpha()

            if self.alphaFrom is not None:
                render.setLocalAlpha(self.alphaFrom)

        if self.node.isActivate() is False:
            self.log("[%s] not active - alphaTo not started" % (self.node.getName()))
            # TIP:  If your node is Arrow's child and Arrow is disable - you can get this error.
            #       Try to do this task after onArrowActivate listened. You can get Arrow by Mengine.getArrow()
            return True

        self.affectorId = self.node.alphaTo(self.time, self.alphaTo, self.easing, self._onAlphaTo)

        if self.affectorId == 0:
            self.log("[%s] not active - affectorId==0" % (self.node.getName()))
            return True

        return False

    def _onFastSkip(self):
        render = self.node.getRender()
        if render is not None:
            if self.isTemp:  # if isTemp restore original alpha
                render.setLocalAlpha(self.alphaOrig)

            else:
                render.setLocalAlpha(self.alphaTo)

        return True

    def _onSkip(self):
        self.affectorId = None

        self.node.colorStop()

        if self.isTemp:  # if isTemp restore original alpha

            render = self.node.getRender()

            if render is not None:
                render.setLocalAlpha(self.alphaOrig)

        elif self.interrupt is False:
            render = self.node.getRender()

            if render is not None:
                render.setLocalAlpha(self.alphaTo)

    def _onAlphaTo(self, node, affectorId, isEnd):
        if self.affectorId != affectorId:
            return

        self.affectorId = None

        self.complete(isSkiped=isEnd is False)

    def _onComplete(self):
        if self.isTemp:  # if isTemp restore original alpha

            render = self.node.getRender()

            if render is not None:
                render.setLocalAlpha(self.alphaOrig)