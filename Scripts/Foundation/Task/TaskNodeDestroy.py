from MixinNode import MixinNode
from Task import Task

class TaskNodeDestroy(MixinNode, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskNodeDestroy, self)._onParams(params)
        pass

    def _onRun(self):
        Menge.destroyNode(self.node)
        self.node = None

        return True
        pass
    pass