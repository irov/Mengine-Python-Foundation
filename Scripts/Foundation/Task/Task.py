from Foundation.Initializer import Initializer
from Foundation.Params import Params

class TaskException(Exception):
    def __init__(self, value):
        self.value = value
        pass

    def __str__(self):
        return str(self.value)
    pass

class ValidateException(Exception):
    def __init__(self, value):
        self.value = value
        pass

    def __str__(self):
        return str(self.value)
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

    def isSkiped(self):
        return self.base.skiped

    def _onFastSkip(self):
        return False

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

        self.base.complete(isRunning, isSkiped)
        pass

    def skip(self):
        if self.base is None:
            return

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
        #print "Task %s onValidate, skiped: %d" % (self.base, self.isSkiped())
        try:
            self._onValidate()
        except Exception as ex:
            self._onValidateFailed(ex)

            return False

        return True

    def _onValidate(self):
        pass

    def validateFailed(self, value):
        raise ValidateException(value)

    def _onValidateFailed(self, ex):
        self.base._traceException("Task %s is not validate %s" % (self.base, ex))
        pass

    def _onInitializeFailed(self, msg):
        self.base._traceError("Task %s is not initialized %s" % (self.base, msg))
        pass

    def _onFinalizeFailed(self, msg):
        self.base._traceError("Task %s is not finalized %s" % (self.base, msg))
        pass

    def invalidTask(self, msg):
        raise TaskException(msg)

    def log(self, msg, *args):
        Trace.log("Task", 0, "TaskChain [%s] Caller %s:%s doc %s | [%s] %s" % (self.base.chain, self.base.caller[0], self.base.caller[1], self.base.caller[2], self.__class__.__name__, msg % args))
        pass
    pass