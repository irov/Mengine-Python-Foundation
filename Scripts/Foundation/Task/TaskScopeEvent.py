from Foundation.Task.MixinEvent import MixinEvent
from Foundation.Task.MixinGroup import MixinGroup
from Foundation.Task.Task import Task
from Foundation.Task.TaskGenerator import TaskGenerator
from Foundation.Task.TaskGenerator import TaskSource

class TaskScopeEvent(MixinGroup, MixinEvent, Task):
    Skiped = False

    def _onParams(self, params):
        super(TaskScopeEvent, self)._onParams(params)

        self.Event = params.get("Event")

        self.Scope = Utils.make_functor(params, "Scope")
        pass

    def _onValidate(self):
        super(TaskScopeEvent, self)._onValidate()

        if isinstance(self.Event, Event) is False:
            self.validateFailed("Event must be Event but is %s" % (self.Event))
            pass

        if callable(self.Scope) is False:
            self.validateFailed("Scope %s is not callable" % (self.Scope))
            pass
        pass

    def _onRun(self):
        self.addEvent(self.Event, self.__onEventFilter)

        return False
        pass

    def __onEventFilter(self, *args, **kwargs):
        base = self.base
        chain = base.chain

        scope = []
        source = TaskSource(scope)

        skiped = self.isSkiped()
        source.setSkiped(skiped)

        result = self.Scope(source, *args, **kwargs)

        if isinstance(result, bool) is False:
            self.log("%s scope %s must return bool [True|False] but return %s" % (self.Event, self.Scope, result))

            return False
            pass

        if result is False:
            return False
            pass

        nexts = self.base.popNexts()

        tg = TaskGenerator(chain, self.Group, scope, base)
        lastTask = tg.parse()

        if lastTask is None:
            self.invalidTask("TaskScopeEvent %s invalid generate scope %s" % (self.Event, self.Scope))
            pass

        for next in nexts:
            lastTask.addNext(next)
            pass

        return True
        pass
    pass