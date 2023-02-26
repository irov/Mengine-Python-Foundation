from MixinNode import MixinNode
from Task import Task

class TaskNodeEnableGlobalMouseEvent(MixinNode, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskNodeEnableGlobalMouseEvent, self)._onParams(params)

        self.value = params.get("Value", True)
        pass

    def _onRun(self):
        self.node.enableGlobalMouseEvent(self.value)

        return True
        pass
    pass