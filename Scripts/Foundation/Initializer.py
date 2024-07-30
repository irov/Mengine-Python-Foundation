class Initializer(object):
    __metaclass__ = baseslots("_initialized")

    def __init__(self):
        super(Initializer, self).__init__()

        self._initialized = None
        pass

    def isInitialized(self):
        return self._initialized is True
        pass

    def onInitialize(self, *args, **kwds):
        if self._initialized is not None:
            if self._initialized is True:
                self.onInitializeFailed("already initialized")
                pass

            if self._initialized is False:
                self.onInitializeFailed("is finalized")
                pass

            return False
            pass

        try:
            self._onInitialize(*args, **kwds)
        except Exception as ex:
            self.onInitializeFailed("onInitialize exception %s\n%s" % (ex, traceback.format_exc()))

            return False
            pass

        self._initialized = True

        return True
        pass

    def _onInitialize(self, *args, **kwds):
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
        pass

    def onFinalize(self):
        if self._initialized is not True:
            if self._initialized is False:
                self.onFinalizeFailed("already finalized")
                pass

            if self._initialized is None:
                self.onFinalizeFailed("not initialized")
                pass

            return
            pass

        self._initialized = False

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
    pass