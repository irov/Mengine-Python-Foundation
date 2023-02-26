from MixinNode import MixinNode
from Task import Task

class TaskNodeSetPosition(MixinNode, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskNodeSetPosition, self)._onParams(params)

        self.value = params.get("Value")
        pass

    def _onRun(self):
        self.node.setLocalPosition(self.value)

        return True
        pass
    pass