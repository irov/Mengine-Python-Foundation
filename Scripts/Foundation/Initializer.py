class Initializer(object):
    __metaclass__ = baseslots("_initialized")

    InitializerReferences = {}

    def __init__(self):
        super(Initializer, self).__init__()

        self._initialized = None
        pass

    def isInitialized(self):
        return self._initialized is not None

    def onInitialize(self, *args, **kwargs):
        if self._initialized is not None:
            self.onInitializeFailed("already initialized")

            return False

        try:
            self._onInitialize(*args, **kwargs)
        except Exception as ex:
            self.onInitializeFailed("onInitialize exception %s\n%s" % (ex, traceback.format_exc()))

            return False

        if _VALIDATION is True:
            Initializer.InitializerReferences.setdefault(self.__class__, []).append(self)

            self._initialized = traceback.extract_stack()
        else:
            self._initialized = True
            pass

        return True

    def _onInitialize(self, *args, **kwargs):
        pass

    def onInitializeFailed(self, msg):
        try:
            self._onInitializeFailed(msg)
        except Exception as ex:
            Trace.log("Object", 0, "Initialize.onInitializeFailed %s exception %s\n%s" % (msg, ex, traceback.format_exc()))
            pass
        pass

    def _onInitializeFailed(self, msg):
        Trace.log("Object", 0, "Initialize._onInitializeFailed %s" % (msg))
        pass

    def initializeFailed(self, msg, *args):
        assert type(msg) == str

        raise Exception(msg % args)

    def onFinalize(self):
        if self._initialized is None:
            self.onFinalizeFailed("not initialized")

            return

        if _VALIDATION is True:
            Initializer.InitializerReferences.setdefault(self.__class__, []).remove(self)
            pass

        self._initialized = None

        try:
            self._onFinalize()
        except Exception as ex:
            self.onFinalizeFailed("onFinalize exception %s\n%s" % (ex, traceback.format_exc()))
            return
        pass

    def _onFinalize(self):
        pass

    def onFinalizeFailed(self, msg):
        try:
            self._onFinalizeFailed(msg)
        except Exception as ex:
            Trace.log("Object", 0, "Initialize.onFinalizeFailed %s exception %s\n%s" % (msg, ex, traceback.format_exc()))
            pass
        pass

    def _onFinalizeFailed(self, msg):
        Trace.log("Object", 0, "Initialize.onFinalizeFailed %s" % (msg))
        pass

    @classmethod
    def validate(cls):
        if _VALIDATION is True:
            print "Validating Initializers..."
            for initializer, objs in Initializer.InitializerReferences.items():
                for obj in objs:
                    print "Initializer '%s' is not finalized, trace:\n%s" % (initializer.__name__, "".join(traceback.format_list(obj._initialized)))
                    pass
                pass
            pass
        pass
    pass