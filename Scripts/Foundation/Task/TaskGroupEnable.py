from Foundation.Task.Task import Task
from Foundation.Task.MixinGroup import MixinGroup

class TaskGroupEnable(MixinGroup, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskGroupEnable, self)._onParams(params)

        self.Value = params.get("Value", True)
        pass

    def _onRun(self):
        Group = self.getGroup()

        if self.Value is True:
            if Group.onEnable() is False:
                self.log("Group '%s' invalid enable" % (Group.getName()))
                pass
        else:
            if Group.onDisable() is False:
                self.log("Group '%s' invalid disable" % (Group.getName()))
                pass
            pass
        pass