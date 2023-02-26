class ParamsException(BaseException):
    def __init__(self, value):
        self.value = value
        pass

    def __str__(self):
        return str(self.value)
        pass
    pass

class DefaultParam(object):
    __slot__ = "value"
    def __init__(self, value):
        self.value = value
        pass
    pass

class Params(object):
    __metaclass__ = baseslots("consts", "params")

    NoDefault = object()
    NotFound = object()

    def __init__(self):
        super(Params, self).__init__()

        self.consts = {}
        self.params = {}
        pass

    @staticmethod
    def declareORM(typeORM):
        pass

    @staticmethod
    def releaseORM(typeORM):
        pass

    if _DEVELOPMENT is False:
        @staticmethod
        def addParam(typeORM, key, paramType=None):
            def __get(self):
                param = self.params[key]

                if isinstance(param, DefaultParam) is True:
                    return param.value
                    pass

                return param
                pass

            def __set(self, value):
                self.setParam(key, value)
                pass

            setattr(typeORM, "get%s" % (key), __get)
            setattr(typeORM, "set%s" % (key), __set)
            pass
        pass
    else:
        @staticmethod
        def addParam(typeORM, key, paramType=None):
            def __get(self):
                param = self.params[key]

                if isinstance(param, DefaultParam) is True:
                    return param.value
                    pass

                return param
                pass

            def __set(self, value):
                if paramType is not None and isinstance(value, paramType) is False:
                    self.paramsFailed("Param %s setup invalid value '%s' need type '%s'" % (key, value, paramType))
                    pass

                self.setParam(key, value)
                pass

            setattr(typeORM, "get%s" % (key), __get)
            setattr(typeORM, "set%s" % (key), __set)
            pass
        pass

    @staticmethod
    def addConst(typeORM, key):
        def __get(self):
            return self.consts[key]
            pass

        def __set(self, value):
            self.paramsFailed("Param %s is const" % (key))
            pass

        setattr(typeORM, "get%s" % (key), __get)
        setattr(typeORM, "set%s" % (key), __set)
        pass

    @staticmethod
    def addResource(typeORM, key):
        def __get(self):
            return self.consts[key]
            pass

        def __set(self, value):
            self.paramsFailed("Resource %s is const" % (key))
            pass

        setattr(typeORM, "get%s" % (key), __get)
        setattr(typeORM, "set%s" % (key), __set)
        pass

    def __extractResource(self, key, value, default):
        if value is None:
            return None
            pass

        if isinstance(value, Menge.Resource) is True:
            return value
            pass

        if isinstance(value, str) is False:
            self.paramsFailed("Param '%s' is not string '%s'" % (key, value))
            return None
            pass

        if Menge.hasResource(value) is False:
            if default is Params.NoDefault:
                self.paramsFailed("Param '%s' is not found resource '%s'" % (key, value))
                return None
                pass
            else:
                return default
                pass
            pass

        resource = Menge.getResourceReference(value)

        return resource
        pass

    def initParam(self, key, params, Default=NoDefault):
        value = None
        if Default is Params.NoDefault:
            value = params[key]
            pass
        else:
            value = params.get(key, Default)
            pass

        self.params[key] = value
        pass

    def initResource(self, key, params, default=NoDefault):
        value = None

        if default is Params.NoDefault:
            value = params[key]
            pass
        else:
            value = params.get(key, default)
            pass

        resource = self.__extractResource(key, value, default)

        self.consts[key] = resource
        pass

    def initConst(self, key, params, default=NoDefault):
        value = None
        if default is Params.NoDefault:
            value = params[key]
        else:
            value = params.get(key, default)
            pass

        self.setConst(key, value)
        pass

    def setConst(self, key, value):
        self.consts[key] = value

        self.__callAction(key, "Update", value)
        pass

    def onParams(self, params):
        try:
            self._onParams(params)
        except ParamsException as pe:
            Trace.log("Manager", 0, "Params.onParams error %s" % (pe))

            return False
            pass

        return True
        pass

    def _onParams(self, params):
        pass

    def onReloadParams(self, params):
        self.onParams(params)
        self._onLoadParams()
        pass

    def hasParam(self, key):
        if key in self.params:
            return True
            pass

        if key in self.consts:
            return True
            pass

        return False
        pass

    def setParam(self, key, value):
        if self.superParam(key, value) is False:
            return False
            pass

        self.__callAction(key, "Update", value)

        return True
        pass

    def superParam(self, key, value):
        if _DEVELOPMENT is True:
            if self.__existParam(key) is False:
                Trace.log("Object", 0, "Params.superParam %s invalid exist param %s value %s type %s" % (self.getName(), key, value, type(value)))

                return False
                pass

            if self.__checkParamValue(value) is False:
                Trace.log("Object", 0, "Params.superParam %s invalid key %s value %s type %s" % (self.getName(), key, value, type(value)))

                return False
                pass
            pass

        self.params[key] = value

        return True
        pass

    def setParams(self, **params):
        for key, value in params.iteritems():
            if self.superParam(key, value) is False:
                return False
                pass

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
                pass

            if self.__checkParamValue(value) is False:
                Trace.log("Object", 0, "Params.appendParam check param value %s - %s:%s" % (self.getName(), key, value))

                return False
                pass
            pass

        param = self.params[key]

        if isinstance(param, DefaultParam) is True:
            param = param.value[:]
            self.params[key] = param
            pass

        index = len(param)
        param.append(value)

        self.__callAction(key, "Append", index, value)

        return True
        pass

    def updateParam(self, key):
        if _DEVELOPMENT is True:
            if self.__existParam(key) is False:
                return False
                pass
            pass

        param = self.params[key]

        self.__callAction(key, "Update", param)

        return True
        pass

    def changeParam(self, key, index, value):
        if _DEVELOPMENT is True:
            if self.__existChangeParam(key, index) is False:
                return False
                pass

            if self.__checkParamValue(value) is False:
                Trace.log("Object", 0, "Params.superParam %s - %s:%s" % (self.getName(), key, value))

                return False
                pass
            pass

        param = self.params[key]

        if isinstance(param, DefaultParam) is True:
            param = param.value[:]
            self.params[key] = param
            pass

        param[index] = value

        self.__callAction(key, "Change", index, value)

        return True
        pass

    def insertParam(self, key, index, value):
        if _DEVELOPMENT is True:
            if self.__existListParam(key) is False:
                return
                pass

            if self.__checkParamValue(value) is False:
                Trace.log("Object", 0, "Params.insertParam %s - %s:%s" % (self.getName(), key, value))

                return False
                pass
            pass

        param = self.params[key]

        if isinstance(param, DefaultParam) is True:
            param = param.value[:]
            self.params[key] = param
            pass

        param.insert(index, value)

        self.__callAction(key, "Append", index, value)
        pass

    def delParam(self, key, value):
        if _DEVELOPMENT is True:
            if self.__existListParam(key) is False:
                return
                pass

            if self.__checkParamValue(value) is False:
                Trace.log("Object", 0, "Params.delParam %s - %s:%s" % (self.getName(), key, value))

                return False
                pass
            pass

        param = self.params[key]

        if isinstance(param, DefaultParam) is True:
            param = param.value[:]
            self.params[key] = param
            pass

        index = param.index(value)

        old = param[:]

        param.remove(value)

        self.__callAction(key, "Remove", index, value, old)
        pass

    def insertDictParam(self, key, pair_0, pair_1):
        """
        'key' is actual param
        'pair_0' is key of dict param to update
        'pair_1' is value by pair_0 key in 'key' dict
        """
        if _DEVELOPMENT is True:
            if self.__existDictParam(key) is False:
                return

            if self.__checkParamValue(pair_0) is False:
                Trace.log("Object", 0, "Params.delParam %s - %s:%s" % (self.getName(), key, pair_0))

                return False

        param = self.params[key]

        if isinstance(param, DefaultParam) is True:
            param = param.value[:]
            self.params[key] = param

        param[pair_0] = pair_1

        self.__callAction(key, "InsertDict", pair_0, pair_1)

    def popDictParam(self, key, pair_0):
        """
        'key' is actual param
        'pair_0' is key of dict param to update
        """
        if _DEVELOPMENT is True:
            if self.__existDictParam(key) is False:
                return

            if self.__checkParamValue(pair_0) is False:
                Trace.log("Object", 0, "Params.delParam %s - %s:%s" % (self.getName(), key, pair_0))

                return False

        param = self.params[key]

        if isinstance(param, DefaultParam) is True:
            param = param.value[:]
            self.params[key] = param

        pair_1 = param.pop(pair_0, None)

        self.__callAction(key, "PopDict", pair_0, pair_1)

    def getParam(self, key):
        const = self.consts.get(key, Params.NotFound)

        if const is not Params.NotFound:
            if isinstance(const, DefaultParam) is True:
                return const.value
                pass

            return const
            pass

        param = self.params.get(key, Params.NotFound)

        if param is not Params.NotFound:
            if isinstance(param, DefaultParam) is True:
                return param.value
                pass

            return param
            pass

        self.paramsFailed("Params '%s' not found key" % (key))

        return None
        pass

    def __existParam(self, key):
        if key not in self.params:
            self.paramsFailed("Params not found key '%s'" % (key))
            return False
            pass

        return True
        pass

    def __existListParam(self, key):
        param = self.getParam(key)

        if param is None:
            self.paramsFailed("Params key '%s' must be list, not 'None'" % (key))
            return False
            pass

        if isinstance(param, list) is False:
            self.paramsFailed("Params key '%s' must be list but not '%s'" % (key, param))
            return False
            pass

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
            pass

        if isinstance(param, DefaultParam) is True:
            param = param.value
            pass

        if isinstance(param, list) is True:
            if len(param) < index:
                self.paramsFailed("Params key '%s' change index %s more list size %d" % (key, len(param), index))

                return False
                pass
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
            pass

        return True
        pass

    def getParams(self):
        return self.params
        pass

    def getConsts(self):
        return self.consts
        pass

    def removeParams(self):
        self.params = {}
        self.consts = {}
        pass

    def __callAction(self, key, type, *value):
        actor = self._getActor()

        if actor is None:
            return False
            pass

        if actor.callAction(key, False, type, *value) is False:
            return False
            pass

        return True
        pass

    def __updateParams(self, params):
        actor = self._getActor()

        if actor is None:
            return
            pass

        actor.callActions(params, False, False, "Update")
        pass

    def _getActor(self):
        return None
        pass

    def paramsFailed(self, msg):
        new_msg = self._paramsFailed(msg)
        raise ParamsException(new_msg)
        pass

    def _paramsFailed(self, msg):
        return msg
        pass

    def __checkParamValue(self, value):
        if value is None:
            return True
            pass
        elif isinstance(value, bool) is True:
            return True
            pass
        elif isinstance(value, int) is True:
            return True
            pass
        elif isinstance(value, long) is True:
            return True
            pass
        elif isinstance(value, float) is True:
            return True
            pass
        elif isinstance(value, str) is True:
            return True
            pass
        elif isinstance(value, unicode) is True:
            return True
            pass
        elif Menge.is_class(value) is True:
            if isinstance(value, Menge.vec2f) is True:
                return True
                pass
            elif isinstance(value, Menge.vec3f) is True:
                return True
                pass
            elif isinstance(value, Menge.ConstString) is True:
                return True
                pass

            return False
            pass
        elif isinstance(value, tuple) is True:
            for v in value:
                if self.__checkParamValue(v) is False:
                    return False
                    pass
                pass

            return True
            pass
        elif isinstance(value, list) is True:
            for v in value:
                if self.__checkParamValue(v) is False:
                    return False
                    pass
                pass

            return True
            pass
        elif isinstance(value, dict) is True:
            for k, v in value.iteritems():
                if self.__checkParamValue(k) is False:
                    return False
                    pass
                if self.__checkParamValue(v) is False:
                    return False
                    pass
                pass

            return True
            pass
        elif self._checkParamExtraValue(value) is True:
            return True
            pass

        return False
        pass

    def _checkParamExtraValue(self, value):
        return True
        pass
    pass