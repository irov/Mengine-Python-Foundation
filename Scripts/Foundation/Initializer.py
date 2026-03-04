class Initializer(object):
    __metaclass__ = baseslots("_initialized")

    if _VALIDATION is True:
        InitializerReferences = {}
        pass

    def __init__(self):
        super(Initializer, self).__init__()

        self._initialized = False
        pass

    def isInitialized(self):
        return self._initialized is True

    def onInitialize(self, *args, **kwargs):
        if self._initialized is True:
            self.onInitializeFailed("already initialized")

            return False

        try:
            self._onInitialize(*args, **kwargs)
        except Exception as ex:
            self.onInitializeFailed(ex)

            return False

        self._initialized = True

        if _VALIDATION is True:
            Initializer.InitializerReferences.setdefault(self.__class__, {})[self] = traceback.extract_stack()
            pass

        return True

    def _onInitialize(self, *args, **kwargs):
        pass

    def onInitializeFailed(self, ex):
        try:
            self._onInitializeFailed(ex)
        except Exception as nex:
            Trace.log_exception("Object", 0, "Initialize.onInitializeFailed %s exception %s" % (ex, nex))
            pass
        pass

    def _onInitializeFailed(self, ex):
        Trace.log_exception("Object", 0, "Initialize._onInitializeFailed %s" % (ex))
        pass

    def initializeFailed(self, msg, *args):
        assert type(msg) == str

        raise Exception(msg % args)

    def onFinalize(self):
        if self._initialized is False:
            self.onFinalizeFailed("not initialized")
            return

        if _VALIDATION is True:
            Initializer.InitializerReferences.setdefault(self.__class__, []).pop(self, None)
            pass

        self._initialized = False

        try:
            self._onFinalize()
        except Exception as ex:
            self.onFinalizeFailed(ex)
            return
        pass

    def _onFinalize(self):
        pass

    def onFinalizeFailed(self, ex):
        try:
            self._onFinalizeFailed(ex)
        except Exception as nex:
            Trace.log_exception("Object", 0, "Initialize.onFinalizeFailed %s exception %s" % (ex, nex))
            pass
        pass

    def _onFinalizeFailed(self, ex):
        Trace.log_exception("Object", 0, "Initialize.onFinalizeFailed %s" % (ex))
        pass

    def getInitializeStack(self):
        if _VALIDATION is True:
            return Initializer.InitializerReferences.get(self.__class__, {}).get(self, None)

        return None

    @classmethod
    def validate(cls):
        if _VALIDATION is True:
            print "Validating Initializers..."
            for initializer, objs in Initializer.InitializerReferences.items():
                for obj, stack in objs.items():
                    trace_lines = ["Initializeback (most recent call last):\n"]

                    for filename, lineno, funcname, _ in stack:
                        trace_lines.append("  File \"%s\", line %s in %s\n" % (filename, lineno, funcname))
                        pass

                    print "Initializer '%s' is not finalized, trace:\n%s" % (initializer.__name__, "".join(trace_lines))
                    pass
                pass
            pass