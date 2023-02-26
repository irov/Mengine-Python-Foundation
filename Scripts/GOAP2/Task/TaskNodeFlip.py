from MixinNode import MixinNode
from Task import Task

class TaskNodeFlip(MixinNode, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskNodeFlip, self)._onParams(params)

        self.value = None
        pass

    def _onRun(self):
        self.value = self.node.getFlipX()

        if self.value is False:
            self.node.setFlipX(True)
            pass

        if self.value is True:
            self.node.setFlipX(False)
            pass

        return True
        pass

    pass