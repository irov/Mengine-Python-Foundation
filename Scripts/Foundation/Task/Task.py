from Foundation.Initializer import Initializer
from Foundation.Params import Params

class TaskException(Exception):
    def __init__(self, value):
        self.value = value
        pass

    def __str__(self):
        return str(self.value)
        pass
    pass

class ValidateException(Exception):
    def __init__(self, value):
        self.value = value
        pass

    def __str__(self):
        return str(self.value)
        pass
    pass

class Task(Params, Initializer):
    __metaclass__ = baseslots("base")

    Skiped = False
    SkipBlock = False

    def __init__(self):
        super(Task, self).__init__()

        self.base = None
        pass

    def setBase(self, base):
        self.base = base
        pass

    def _onCheck(self):
        return True
        pass

    def _onCheckSkip(self):
        pass

    def _onInitialize(self):
        super(Task, self)._onInitialize()
        pass

    def _onFinalize(self):
        super(Task, self)._onFinalize()

        self.base = None
        pass

    def _onRun(self):
        return True
        pass

    def isSkiped(self):
        return self.base.skiped
        pass

    def _onFastSkip(self):
        return False
        pass

    def _onSkip(self):
        pass

    def _onSkipNoSkiped(self):
        pass

    def _onSkipBlock(self):
        pass

    def _onCancel(self):
        pass

    def complete(self, isRunning=True, isSkiped=False):
        if self.base is None:
            return
            pass

        self.base.complete(isRunning, isSkiped)
        pass

    def skip(self):
        if self.base is None:
            return
            pass

        self.base.skip()
        pass

    def setError(self, value):
        self.base.setError(value)
        pass

    def _onComplete(self):
        pass

    def _onFinally(self):
        pass

    def onValidate(self):
        if self.isSkiped() is True:
            return True
            pass

        try:
            self._onValidate()
        except Exception as ex:
            traceback.print_exc()

            self._onValidateFailed(ex)

            return False
            pass

        return True
        pass

    def _onValidate(self):
        pass

    def validateFailed(self, value):
        raise ValidateException(value)
        pass

    def _onValidateFailed(self, ex):
        self.base._traceError("Task %s is not validate %s" % (self.base, ex))
        pass

    def _onInitializeFailed(self, msg):
        self.base._traceError("Task %s is not initialized %s" % (self.base, msg))
        pass

    def _onFinalizeFailed(self, msg):
        self.base._traceError("Task %s is not finalized %s" % (self.base, msg))
        pass

    def invalidTask(self, msg):
        raise TaskException(msg)
        pass

    def log(self, msg, *args):
        Trace.log("Task", 0, "TaskChain [%s] Caller %s:%s doc %s | [%s] %s" % (self.base.chain, self.base.caller[0], self.base.caller[1], self.base.caller[2], self.__class__.__name__, msg % args))
        pass
    pass