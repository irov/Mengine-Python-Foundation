class ParamsException(BaseException):
    def __init__(self, value):
        self.value = value
        pass

    def __str__(self):
        return str(self.value)
    pass

class DefaultParam(object):
    __slot__ = "value"

    def __init__(self, value):
        self.value = value
        pass
    pass

class WidgetParam(object):
    def __init__(self, Type, ReadOnly, Description, Step):
        self.Type = Type
        self.ReadOnly = ReadOnly
        self.Description = Description
        self.Step = 0.0 if Step is None else Step
        pass

    def getType(self):
        return self.Type

    def isReadOnly(self):
        return self.ReadOnly

    def getDescription(self):
        return self.Description

    def getStep(self):
        return self.Step
    pass

class WidgetParamCheckBox(WidgetParam):
    def __init__(self, ReadOnly=False, Description=None, Step=None):
        super(WidgetParamCheckBox, self).__init__(Mengine.LEWT_CHECKBOX, ReadOnly, Description, Step)
        pass
    pass

class WidgetParamPosition(WidgetParam):
    def __init__(self,  ReadOnly=False, Description=None, Step=0.001):
        super(WidgetParamPosition, self).__init__(Mengine.LEWT_POSITION, ReadOnly, Description, Step)
        pass
    pass

class WidgetParamScale(WidgetParam):
    def __init__(self, ReadOnly=False, Description=None, Step=0.001):
        super(WidgetParamScale, self).__init__(Mengine.LEWT_SCALE, ReadOnly, Description, Step)
        pass
    pass

class WidgetParamOrientation(WidgetParam):
    def __init__(self, ReadOnly=False, Description=None, Step=0.0174533):
        super(WidgetParamOrientation, self).__init__(Mengine.LEWT_ORIENTATION, ReadOnly, Description, Step)
        pass
    pass

class WidgetParamAlpha(WidgetParam):
    def __init__(self, ReadOnly=False, Description=None, Step=0.01):
        super(WidgetParamAlpha, self).__init__(Mengine.LEWT_ALPHA, ReadOnly, Description, Step)
        pass
    pass

class WidgetParamRGB(WidgetParam):
    def __init__(self, ReadOnly=False, Description=None, Step=0.01):
        super(WidgetParamRGB, self).__init__(Mengine.LEWT_RGB, ReadOnly, Description, Step)
        pass
    pass

class ParamsEnum(object):
    ACTION_UPDATE = 0
    ACTION_APPEND = 1
    ACTION_REMOVE = 2
    ACTION_CHANGE = 3
    ACTION_INSERT_DICT = 4
    ACTION_POP_DICT = 5
    pass

class Params(object):
    __metaclass__ = baseslots("params")

    NoDefault = object()
    NotFound = object()

    def __init__(self):
        super(Params, self).__init__()

        self.params = {}
        pass

    @staticmethod
    def declareORM(typeORM):
        pass

    if _DEVELOPMENT is False:
        @classmethod
        def declareParam(cls, key, ParamType=None, Widget=None):
            def __get(self):
                param = self.params[key]

                if isinstance(param, DefaultParam) is True:
                    return param.value

                return param

            def __set(self, value):
                self.setParam(key, value)
                pass

            setattr(cls, "get%s" % (key), __get)
            setattr(cls, "set%s" % (key), __set)
            pass
        pass
    else:
        @classmethod
        def declareParam(cls, key, ParamType=None, Widget=None):
            def __get(self):
                param = self.params[key]

                if isinstance(param, DefaultParam) is True:
                    return param.value

                return param

            def __set(self, value):
                if ParamType is not None and isinstance(value, ParamType) is False:
                    self.paramsFailed("Param %s setup invalid value '%s' need type '%s'" % (key, value, ParamType))
                    pass

                self.setParam(key, value)
                pass

            setattr(cls, "get%s" % (key), __get)
            setattr(cls, "set%s" % (key), __set)

            if Widget is not None:
                PARAMS_WIDGETS = getattr(cls, "PARAMS_WIDGETS", {})
                PARAMS_WIDGETS[key] = Widget
                setattr(cls, "PARAMS_WIDGETS", PARAMS_WIDGETS)
                pass
            pass
        pass

    @classmethod
    def declareConst(cls, key):
        def __get(self):
            return self.params[key]

        def __set(self, value):
            self.paramsFailed("Param %s is const" % (key))
            pass

        setattr(cls, "get%s" % (key), __get)
        setattr(cls, "set%s" % (key), __set)
        pass

    @classmethod
    def declareResource(cls, key):
        def __get(self):
            return self.params[key]

        def __set(self, value):
            self.paramsFailed("Resource %s is const" % (key))
            pass

        setattr(cls, "get%s" % (key), __get)
        setattr(cls, "set%s" % (key), __set)
        pass

    def __extractResource(self, key, value, default):
        if value is None:
            return None

        if isinstance(value, Mengine.Resource) is True:
            return value

        if isinstance(value, str) is False:
            self.paramsFailed("Param '%s' is not string '%s'" % (key, value))
            return None

        if Mengine.hasResource(value) is False:
            if default is Params.NoDefault:
                self.paramsFailed("Param '%s' is not found resource '%s'" % (key, value))
                return None
            else:
                return default

        resource = Mengine.getResourceReference(value)

        return resource

    def initParam(self, key, params, default=NoDefault):
        if default is Params.NoDefault:
            value = params[key]
            pass
        else:
            value = params.get(key, default)
            pass

        self.params[key] = value
        pass

    def initResource(self, key, params, default=NoDefault):
        if default is Params.NoDefault:
            value = params[key]
            pass
        else:
            value = params.get(key, default)
            pass

        resource = self.__extractResource(key, value, default)

        self.params[key] = resource
        pass

    def initConst(self, key, params, default=NoDefault):
        if default is Params.NoDefault:
            value = params[key]
        else:
            value = params.get(key, default)
            pass

        self.setConst(key, value)
        pass

    def setConst(self, key, value):
        self.params[key] = value

        self.__callAction(ParamsEnum.ACTION_UPDATE, key, value)
        pass

    def onParams(self, params):
        try:
            self._onParams(params)

            if _DEVELOPMENT is True:
                self._onCheckParams()
                pass
        except ParamsException as pe:
            Trace.log("Manager", 0, "Params.onParams error %s" % (pe))

            return False

        return True

    def _onCheckParams(self):
        pass

    def _onParams(self, params):
        pass

    def onReloadParams(self, params):
        self.onParams(params)
        self._onLoadParams()
        pass

    def hasParam(self, key):
        return key in self.params

    def setParam(self, key, value):
        if self.superParam(key, value) is False:
            return False

        self.__callAction(ParamsEnum.ACTION_UPDATE, key, value)

        return True

    def superParam(self, key, value):
        if _DEVELOPMENT is True:
            if self.__existParam(key) is False:
                Trace.log("Object", 0, "Params.superParam %s invalid exist param %s value %s type %s" % (self.getName(), key, value, type(value)))

                return False

            if self.__checkParamValue(value) is False:
                Trace.log("Object", 0, "Params.superParam %s invalid key %s value %s type %s" % (self.getName(), key, value, type(value)))

                return False
            pass

        self.params[key] = value

        return True

    def setParams(self, **params):
        for key, value in params.iteritems():
            if self.superParam(key, value) is False:
                return False

            self.params[key] = value
            pass

        self.__updateParams(params)
        pass

    def loadParams(self, params):
        self.params.update(params)

        self._onLoadParams()
        pass

    def _onLoadParams(self):
        pass

    def appendParam(self, key, value):
        if _DEVELOPMENT is True:
            if self.__existListParam(key) is False:
                Trace.log("Object", 0, "Params.appendParam exist list param %s - %s:%s" % (self.getName(), key, value))

                return False

            if self.__checkParamValue(value) is False:
                Trace.log("Object", 0, "Params.appendParam check param value %s - %s:%s" % (self.getName(), key, value))

                return False
            pass

        param = self.params[key]

        if isinstance(param, DefaultParam) is True:
            param = param.value[:]
            self.params[key] = param
            pass

        index = len(param)
        param.append(value)

        self.__callAction(ParamsEnum.ACTION_APPEND, key, index, value)

        return True

    def updateParam(self, key):
        if _DEVELOPMENT is True:
            if self.__existParam(key) is False:
                return False
                pass
            pass

        value = self.params[key]

        self.__callAction(ParamsEnum.ACTION_UPDATE, key, value)

        return True

    def changeParam(self, key, index, value):
        if _DEVELOPMENT is True:
            if self.__existChangeParam(key, index) is False:
                return False

            if self.__checkParamValue(value) is False:
                Trace.log("Object", 0, "Params.superParam %s - %s:%s" % (self.getName(), key, value))

                return False
            pass

        param = self.params[key]

        if isinstance(param, DefaultParam) is True:
            param = param.value[:]
            self.params[key] = param
            pass

        param[index] = value

        self.__callAction(ParamsEnum.ACTION_CHANGE, key, index, value)

        return True

    def insertParam(self, key, index, value):
        if _DEVELOPMENT is True:
            if self.__existListParam(key) is False:
                return

            if self.__checkParamValue(value) is False:
                Trace.log("Object", 0, "Params.insertParam %s - %s:%s" % (self.getName(), key, value))

                return False
            pass

        param = self.params[key]

        if isinstance(param, DefaultParam) is True:
            param = param.value[:]
            self.params[key] = param
            pass

        param.insert(index, value)

        self.__callAction(ParamsEnum.ACTION_APPEND, key, index, value)
        pass

    def delParam(self, key, value):
        if _DEVELOPMENT is True:
            if self.__existListParam(key) is False:
                return

            if self.__checkParamValue(value) is False:
                Trace.log("Object", 0, "Params.delParam %s - %s:%s" % (self.getName(), key, value))

                return False
            pass

        param = self.params[key]

        if isinstance(param, DefaultParam) is True:
            param = param.value[:]
            self.params[key] = param
            pass

        index = param.index(value)

        old = param[:]

        param.remove(value)

        self.__callAction(ParamsEnum.ACTION_REMOVE, key, index, value, old)
        pass

    def insertDictParam(self, key, dict_key, dict_value):
        if _DEVELOPMENT is True:
            if self.__existDictParam(key) is False:
                return

            if self.__checkParamValue(dict_key) is False:
                Trace.log("Object", 0, "Params.insertDictParam %s - %s:%s" % (self.getName(), key, dict_key))
                return

            if self.__checkParamValue(dict_value) is False:
                Trace.log("Object", 0, "Params.insertDictParam %s - %s:%s" % (self.getName(), key, dict_value))
                return

        param = self.params[key]

        if isinstance(param, DefaultParam) is True:
            param = param.value[:]
            self.params[key] = param

        param[dict_key] = dict_value

        self.__callAction(ParamsEnum.ACTION_INSERT_DICT, key, dict_key, dict_value)

    def popDictParam(self, key, dict_key):
        if _DEVELOPMENT is True:
            if self.__existDictParam(key) is False:
                return

            if self.__checkParamValue(dict_key) is False:
                Trace.log("Object", 0, "Params.popDictParam %s - %s:%s" % (self.getName(), key, dict_key))
                return

        param = self.params[key]

        if isinstance(param, DefaultParam) is True:
            param = param.value[:]
            self.params[key] = param

        dict_value = param.pop(dict_key, None)

        self.__callAction(ParamsEnum.ACTION_POP_DICT, key, dict_key, dict_value)

    def getParam(self, key):
        param = self.params.get(key, Params.NotFound)

        if param is Params.NotFound:
            self.paramsFailed("Params '%s' not found key" % (key))

            return None

        if isinstance(param, DefaultParam) is True:
            return param.value

        return param

    def __existParam(self, key):
        if key not in self.params:
            self.paramsFailed("Params not found key '%s'" % (key))
            return False

        return True

    def __existListParam(self, key):
        param = self.getParam(key)

        if param is None:
            self.paramsFailed("Params key '%s' must be list, not 'None'" % (key))
            return False

        if isinstance(param, list) is False:
            self.paramsFailed("Params key '%s' must be list but not '%s'" % (key, param))
            return False

        return True
        pass

    def __existDictParam(self, key):
        param = self.getParam(key)

        if param is None:
            self.paramsFailed("Params key '%s' must be list, not 'None'" % key)
            return False

        if isinstance(param, dict) is False:
            self.paramsFailed("Params key '%s' must be dict but not '%s'" % (key, param))
            return False

        return True

    def __existChangeParam(self, key, index):
        param = self.params.get(key)

        if param is None:
            self.paramsFailed("Params key '%s' must be [list, dict], not 'None'" % (key))

            return False

        if isinstance(param, DefaultParam) is True:
            param = param.value
            pass

        if isinstance(param, list) is True:
            if len(param) < index:
                self.paramsFailed("Params key '%s' change index %s more list size %d" % (key, len(param), index))

                return False
            pass
        elif isinstance(param, dict) is True:
            # if index not in param:
            #     self._paramsFailed("Params key '%s' change index %s not found in dict" % (key, index))
            #     return False
            #     pass
            pass
        else:
            self.paramsFailed("Params key '%s' must be [list, dict] but not %s" % (key, param))

            return False

        return True

    def getParams(self):
        return self.params

    def removeParams(self):
        self.params = {}
        pass

    def __callAction(self, mode, key, *args):
        actor = self._getActor()

        if actor is None:
            return False

        actor.callAction(mode, key, False, *args)

        return True

    def __updateParams(self, params):
        actor = self._getActor()

        if actor is None:
            return

        actor.updateActions(params, False, False)
        pass

    def _getActor(self):
        return None

    def paramsFailed(self, msg):
        new_msg = self._paramsFailed(msg)
        raise ParamsException(new_msg)

    def _paramsFailed(self, msg):
        return msg

    def __checkParamValue(self, value):
        if value is None:
            return True
        elif isinstance(value, bool) is True:
            return True
        elif isinstance(value, int) is True:
            return True
        elif isinstance(value, long) is True:
            return True
        elif isinstance(value, float) is True:
            return True
        elif isinstance(value, str) is True:
            return True
        elif isinstance(value, unicode) is True:
            return True
        elif isinstance(value, tuple) is True:
            for v in value:
                if self.__checkParamValue(v) is False:
                    return False
                pass

            return True
        elif isinstance(value, list) is True:
            for v in value:
                if self.__checkParamValue(v) is False:
                    return False
                pass

            return True
        elif isinstance(value, dict) is True:
            for k, v in value.iteritems():
                if self.__checkParamValue(k) is False:
                    return False
                if self.__checkParamValue(v) is False:
                    return False
                pass

            return True
        elif Mengine.is_class(value) is True:
            if isinstance(value, Mengine.vec2f) is True:
                return True
            elif isinstance(value, Mengine.vec3f) is True:
                return True
            elif isinstance(value, Mengine.ConstString) is True:
                return True

            return False
        elif self._checkParamExtraValue(value) is True:
            return True

        return False

    def _checkParamExtraValue(self, value):
        return True
    pass