from Foundation.Task.MixinGroup import MixinGroup
from Foundation.Task.Task import Task
from Foundation.Task.TaskGenerator import TaskGenerator
from Foundation.Task.TaskGenerator import TaskSource

class TaskScopeSwitch(MixinGroup, Task):
    __metaclass__ = finalslots("Scopes", "Cb", "switched")

    Skiped = True

    def __init__(self):
        super(TaskScopeSwitch, self).__init__()

        self.switched = False
        pass

    def _onParams(self, params):
        super(TaskScopeSwitch, self)._onParams(params)

        self.Scopes = params.get("Scopes")

        self.Cb = Utils.make_functor(params, "Cb")
        pass

    def _onValidate(self):
        super(TaskScopeSwitch, self)._onValidate()

        for Name, Scope in self.Scopes.iteritems():
            if callable(Scope) is False:
                self.validateFailed("State '%s' scope '%s' is not callable" % (Name, Scope))
                pass
            pass
        pass

    def _onRun(self):
        skiped = self.isSkiped()

        self.Cb(skiped, self._onSwitch)

        return False
        pass

    def _onSwitch(self, isSkip, switchId, *Args, **Kwargs):
        if self.isInitialized() is False:
            self.log("_onSwitch already finalized")
            return
            pass

        if self.switched is True:
            self.log("_onSwitch already switched!")
            return
            pass

        if switchId not in self.Scopes:
            self.log("_onSwitch id '%s' not found" % (switchId))
            return
            pass

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
        pass

    def _onFinalize(self):
        super(TaskScopeSwitch, self)._onFinalize()

        self.Scopes = None

        self.Cb = None
        pass
    pass