from Foundation.Task.MixinObserver import MixinObserver
from Foundation.Task.Task import Task
from Notification import Notification

class TaskListener(MixinObserver, Task):
    Skiped = False

    def _onParams(self, params):
        super(TaskListener, self)._onParams(params)

        self.ID = params.get("ID")

        self.Check = Utils.make_functor(params, "Check")
        self.Filter = Utils.make_functor(params, "Filter")

        self.Capture = params.get("Capture", None)
        pass

    def _onValidate(self):
        super(TaskListener, self)._onValidate()

        if Notification.validateIdentity(self.ID) is False:
            self.validateFailed("invalidate id %s" % self.ID)
            pass
        pass

    def _onFinalize(self):
        super(TaskListener, self)._onFinalize()

        self.Filter = None
        pass

    def _onCheck(self):
        if self.Check is not None:
            if self.Check() is True:
                return False
                pass
            pass

        return True
        pass

    def _onRun(self):
        self.addObserver(self.ID, self._onNotifyFilter)

        return False
        pass

    def _onNotifyFilter(self, *args, **kwargs):
        if self.Filter is not None:
            if _DEVELOPMENT is True:
                if Utils.is_valid_functor_args(self.Filter, len(args) + len(kwargs)) is False:
                    self.log("%s filter %s is bad arguments or kwargs" % (self.ID, self.Filter))

                    return False
                    pass
                pass

            result = self.Filter(*args, **kwargs)

            if isinstance(result, bool) is False:
                self.log("%s filter %s must return bool [True|False] but return %s" % (self.ID, self.Filter, result))

                return False
                pass

            if result is False:
                return False
                pass
            pass

        if self.Capture is not None:
            self.Capture.setValue(*args, **kwargs)
            pass

        return True
        pass
    pass