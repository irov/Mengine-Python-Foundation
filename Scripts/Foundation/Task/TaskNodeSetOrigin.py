from MixinNode import MixinNode
from Task import Task

class TaskNodeSetOrigin(MixinNode, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskNodeSetOrigin, self)._onParams(params)

        self.value = params.get("Value")
        pass

    def _onRun(self):
        self.node.setOrigin(self.value)

        return True
        pass
    pass