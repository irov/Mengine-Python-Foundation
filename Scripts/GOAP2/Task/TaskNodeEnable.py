from MixinNode import MixinNode
from Task import Task

class TaskNodeEnable(MixinNode, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskNodeEnable, self)._onParams(params)

        self.value = params.get("Value", True)
        pass

    def _onRun(self):
        if self.value is True:
            self.node.enable()
        else:
            self.node.disable()
            pass

        return True
        pass
    pass