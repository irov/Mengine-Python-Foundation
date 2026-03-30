from Foundation.Task.MixinGroup import MixinGroup
from Foundation.Task.Task import Task
from Foundation.Task.TaskGenerator import TaskSource
from Foundation.TaskManager import TaskManager

class TaskForkSource(MixinGroup, Task):
    __metaclass__ = finalslots("Source")

    Skiped = True

    def _onParams(self, params):
        super(TaskForkSource, self)._onParams(params)

        self.Source = params.get("Source")
        pass

    def _onValidate(self, params):
        super(TaskForkSource, self)._onValidate(params)

        if self.Source is None:
            self.invalidTask("Source param is None")
            pass
        pass

    def _onRun(self):
        taskChain = TaskManager.createTaskChain(Caller=self.base.caller, Group=self.Group)

        taskChain.setSource(self.Source)

        taskChain.run()

        return True