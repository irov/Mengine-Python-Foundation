from Foundation.Task.MixinGroup import MixinGroup
from Foundation.Task.Task import Task
from Foundation.Task.TaskGenerator import TaskGenerator
from Foundation.Task.TaskGenerator import TaskSource

class TaskScopeSwitch(MixinGroup, Task):
    __metaclass__ = finalslots("Scopes", "Switch", "switched")

    Skiped = True

    def __init__(self):
        super(TaskScopeSwitch, self).__init__()

        self.switched = False
        pass

    def _onParams(self, params):
        super(TaskScopeSwitch, self)._onParams(params)

        self.Scopes = params.get("Scopes")

        self.Switch = Utils.make_functor(params, "Switch")
        pass

    def _onValidate(self, params):
        super(TaskScopeSwitch, self)._onValidate(params)

        for Name, Scope in self.Scopes.iteritems():
            if callable(Scope) is False:
                self.validateFailed(params, "State '%s' scope '%s' is not callable" % (Name, Scope))
                pass
            pass
        pass

    def _onRun(self):
        skiped = self.isSkiped()

        self.Switch(skiped, self._onSwitch)

        return False

    def _onSwitch(self, isSkip, switchId, *Args, **Kwargs):
        if self.isInitialized() is False:
            self.invalidTask("_onSwitch already finalized")
            return

        if self.switched is True:
            self.invalidTask("_onSwitch already switched!")
            return

        if switchId not in self.Scopes:
            self.invalidTask("_onSwitch id '%s' not found" % (switchId))
            return

        Scope = self.Scopes[switchId]

        self.switched = True

        base = self.base
        chain = base.chain

        scope = []
        source = TaskSource(scope)

        skiped = self.isSkiped()
        source.setSkiped(skiped)

        Scope(source, *Args, **Kwargs)

        nexts = self.base.popNexts()

        tg = TaskGenerator(chain, self.Group, scope, base)
        lastTask = tg.parse()

        if lastTask is None:
            self.invalidTask("TaskScopeSwitch %s invalid generate scope %s" % (switchId, Scope))
            pass

        for next in nexts:
            lastTask.addNext(next)
            pass

        if isSkip is False:
            self.complete()
            pass

        return True

    def _onFinalize(self):
        super(TaskScopeSwitch, self)._onFinalize()

        self.Scopes = None

        self.Switch = None
        pass
    pass