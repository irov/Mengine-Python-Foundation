class BaseProvider(object):
    s_name = None
    s_methods = {}
    s_allowed_methods = []
    trace_level = 0

    @classmethod
    def _isMethodsValid(cls, methods):
        is_valid = True

        for name, method in methods.items():
            if name not in cls.s_allowed_methods:
                Trace.log("Provider", 0, "Unknown method {!r} ({})".format(name, method))
                is_valid = False

        return is_valid

    @classmethod
    def setProvider(cls, name, methods):
        if _DEVELOPMENT is True:
            if isinstance(methods, dict) is False:
                Trace.log("Provider", 0, "Wrong type {} must be dict".format(type(methods)))
                return False

            if cls._isMethodsValid(methods) is False:
                return False

        cls.s_methods = methods
        cls.s_name = name

        return True

    @classmethod
    def setDevProvider(cls):
        if _DEVELOPMENT is False:
            return
        cls._setDevProvider()

    @staticmethod
    def _setDevProvider():
        pass

    @classmethod
    def getName(cls):
        return cls.s_name

    @classmethod
    def removeProvider(cls):
        cls.s_name = None
        cls.s_methods = {}

    @classmethod
    def _call(cls, name, *args, **kwargs):
        fn = cls.s_methods.get(name)

        if fn is None:
            return cls.__callNotFoundCb(name, *args, **kwargs)

        try:
            return fn(*args, **kwargs)
        except Exception as e:
            return cls.__callException(e, name, *args, **kwargs)


    @classmethod
    def __callNotFoundCb(cls, name, *args, **kwargs):
        fail_cb_name = "_{}NotFoundCb".format(name)
        fail_cb = getattr(cls, fail_cb_name, None)
        if callable(fail_cb) is True:
            return fail_cb(*args, **kwargs)

        Trace.log("Provider", cls.trace_level, "Provider {} Not found method {} in {}".format(cls.s_name, name, cls.s_methods))

    @classmethod
    def __callException(cls, e, name, *args, **kwargs):
        exception_cb_name = "_{}ExceptionCb".format(name)
        exception_cb = getattr(cls, exception_cb_name, None)
        if callable(exception_cb) is True:
            return exception_cb(e, *args, **kwargs)

        raise e

    @classmethod
    def hasMethod(cls, name):
        return name in cls.s_methods

    @classmethod
    def hasProvider(cls):
        return cls.s_name is not None
