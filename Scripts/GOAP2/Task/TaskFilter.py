from GOAP2.Task.MixinObject import MixinObject
from GOAP2.Task.MixinObserver import MixinObserver
from GOAP2.Task.Task import Task
from Notification import Notification

class TaskFilter(MixinObject, MixinObserver, Task):
    def _onParams(self, params):
        super(TaskFilter, self)._onParams(params)

        self.id = params.get("ID")
        self.filter = params.get("Filter")
        pass

    def _onInitialize(self):
        super(TaskFilter, self)._onInitialize()

        if _DEVELOPMENT is True:
            if self.id is None:
                self.initializeFailed("TaskFilter invalid id")
                pass

            if Notification.validateIdentity(self.id) is False:
                self.initializeFailed("TaskFilter invalidate id %s" % (self.id))
                pass
            pass
        pass

    def _onRun(self):
        self.addObserverFilter(self.id, self._onNotifyFilter, self.Object)

        return False
        pass

    def _onNotifyFilter(self, obj, *args):
        result = self.filter(obj, *args)

        if isinstance(result, bool) is False:
            Trace.log("TaskListener", 0, "TaskListener %s invalid filter %s" % (self.name, self.filter))
            return False
            pass

        if result is False:
            return False
            pass

        return True
        pass
    pass