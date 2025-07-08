from Foundation.Task.MixinGroup import MixinGroup
from Foundation.Task.MixinObserver import MixinObserver
from Foundation.Task.Task import Task
from Foundation.Task.TaskGenerator import TaskGenerator
from Foundation.Task.TaskGenerator import TaskSource
from Notification import Notification

class TaskScopeListener(MixinGroup, MixinObserver, Task):
    Skiped = False

    def _onParams(self, params):
        super(TaskScopeListener, self)._onParams(params)

        self.ID = params.get("ID")

        self.Scope = Utils.make_functor(params, "Scope")

        self.Capture = params.get("Capture", None)
        pass

    def _onValidate(self):
        super(TaskScopeListener, self)._onValidate()

        if Notification.validateIdentity(self.ID) is False:
            self.validateFailed("invalidate id %s" % (self.ID))
            pass

        if callable(self.Scope) is False:
            self.validateFailed("Scope %s is not callable" % (self.Scope))
            pass
        pass

    def _onRun(self):
        self.addObserver(self.ID, self._onNotifyFilter)

        return False
        pass

    def _onNotifyFilter(self, *args, **kwargs):
        base = self.base
        chain = base.chain

        scope = []
        source = TaskSource(scope)

        skiped = self.isSkiped()
        source.setSkiped(skiped)

        result = self.Scope(source, *args, **kwargs)

        if isinstance(result, bool) is False:
            self.log("%s scope %s must return bool [True|False] but return %s" % (self.ID, self.Scope, result))

            return False
            pass

        if result is False:
            return False
            pass

        if self.Capture is not None:
            self.Capture.setValue(*args, **kwargs)
            pass

        nexts = self.base.popNexts()

        tg = TaskGenerator(chain, self.Group, scope, base)
        lastTask = tg.parse()

        if lastTask is None:
            self.invalidTask("%s invalid generate scope %s" % (self.ID, self.Scope))
            pass

        for next in nexts:
            lastTask.addNext(next)
            pass

        return True
        pass
    pass