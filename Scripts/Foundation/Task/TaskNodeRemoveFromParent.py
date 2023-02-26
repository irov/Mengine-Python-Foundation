from Foundation.Task.MixinNode import MixinNode

from Task import Task

class TaskNodeRemoveFromParent(MixinNode, Task):
    Skiped = True

    def _onRun(self):
        self.node.removeFromParent()

        return True
        pass
    pass