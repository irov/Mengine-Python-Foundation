from Foundation.Task.MixinGroup import MixinGroup
from Foundation.Task.Task import Task
from Foundation.Task.TaskGenerator import TaskSource
from Foundation.TaskManager import TaskManager

class TaskForkScope(MixinGroup, Task):
    __metaclass__ = finalslots("Scope")

    Skiped = True

    def _onParams(self, params):
        super(TaskForkScope, self)._onParams(params)

        self.Scope = Utils.make_functor(params, "Scope")
        pass

    def _onValidate(self, params):
        super(TaskForkScope, self)._onValidate(params)

        if self.Scope is not None:
            if callable(self.Scope) is False:
                self.validateFailed(params, "Scope %s is not callable" % (self.Scope))
                pass

            if Utils.is_valid_functor_args(self.Scope, 1) is False:
                self.validateFailed(params, "Scope %s is bad arguments or kwargs" % (self.Scope))
                pass
            pass
        pass

    def _onRun(self):
        taskChain = TaskManager.createTaskChain(Caller=self.base.caller, Group=self.Group)

        scope = []
        source = TaskSource(scope)

        skiped = self.isSkiped()
        source.setSkiped(skiped)

        if self.Scope(source) is False:  # scope function returns False
            self.invalidTask("TaskScope invalid make scope")
            pass

        taskChain.setSource(scope)

        taskChain.run()

        return True
    pass