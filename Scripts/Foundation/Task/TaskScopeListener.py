from Foundation.Task.MixinGroup import MixinGroup
from Foundation.Task.MixinObserver import MixinObserver
from Foundation.Task.Task import Task
from Foundation.Task.TaskGenerator import TaskGenerator
from Foundation.Task.TaskGenerator import TaskSource

class TaskScopeListener(MixinGroup, MixinObserver, Task):
    Skiped = False

    def _onParams(self, params):
        super(TaskScopeListener, self)._onParams(params)

        self.ID = params.get("ID")

        self.Scope = Utils.make_functor(params, "Scope")

        self.Check = Utils.make_functor(params, "Check")
        self.Filter = Utils.make_functor(params, "Filter")

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

    def _onFinalize(self):
        super(TaskScopeListener, self)._onFinalize()

        self.Scope = None

        self.Check = None
        self.Filter = None
        self.Capture = None
        pass

    def _onCheck(self):
        if self.Check is not None:
            if self.Check() is True:
                return False

        return True

    def _onRun(self):
        self.addObserver(self.ID, self._onNotifyFilter)

        return False

    def _onNotifyFilter(self, *args, **kwargs):
        if self.Filter is not None:
            if _DEVELOPMENT is True:
                if Utils.is_valid_functor_args(self.Filter, len(args) + len(kwargs)) is False:
                    self.log("%s filter %s is bad arguments or kwargs" % (self.ID, self.Filter))

                    return False

                result = self.Filter(*args, **kwargs)

                if isinstance(result, bool) is False:
                    self.log("%s filter %s must return bool [True|False] but return %s" % (self.ID, self.Filter, result))

                    return False

                if result is False:
                    return False
            else:
                if self.Filter(*args, **kwargs) is False:
                    return False

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

        if result is False:
            return False

        if self.Capture is not None:
            self.Capture.setValue(self.ID, *args, **kwargs)
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