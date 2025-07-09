from Foundation.Task.MixinGroup import MixinGroup
from Foundation.Task.Task import Task
from Foundation.Task.TaskGenerator import TaskGenerator
from Foundation.Task.TaskGenerator import TaskSource

class TaskScope(MixinGroup, Task):
    __metaclass__ = finalslots("Scope")

    Skiped = True

    def _onParams(self, params):
        super(TaskScope, self)._onParams(params)

        self.Scope = Utils.make_functor(params, "Scope")
        pass

    def _onValidate(self):
        super(TaskScope, self)._onValidate()

        if Utils.is_valid_functor_args(self.Scope, 1) is False:
            self.validateFailed("Scope %s is bad arguments or kwargs" % (self.Scope))
            pass
        pass

    def _onRun(self):
        base = self.base
        chain = base.chain

        scope = []
        source = TaskSource(scope)

        skiped = self.isSkiped()
        source.setSkiped(skiped)

        if self.Scope(source) is False:  # scope function returns False
            self.invalidTask("TaskScope invalid make scope")
            pass

        if self.base is None:
            return True
            pass

        nexts = base.popNexts()

        tg = TaskGenerator(chain, self.Group, scope, base)
        lastTask = tg.parse()

        if lastTask is None:
            self.invalidTask("TaskScope invalid generate scope")
            pass

        for next in nexts:
            lastTask.addNext(next)
            pass

        return True
        pass
    pass