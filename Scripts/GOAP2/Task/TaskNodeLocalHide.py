from MixinNode import MixinNode
from Task import Task

class TaskNodeLocalHide(MixinNode, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskNodeLocalHide, self)._onParams(params)

        self.value = params.get("Value", True)
        pass

    def _onRun(self):
        self.node.localHide(self.value)

        return True
        pass
    pass