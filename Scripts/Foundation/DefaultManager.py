import Keys

from DatabaseManager import DatabaseManager

class DefaultManager(object):
    s_defaults = {}
    s_initialize = False

    @staticmethod
    def onInitialize():
        pass

    @staticmethod
    def onFinalize():
        DefaultManager.s_defaults = {}
        pass

    @staticmethod
    def isInitialize():
        return DefaultManager.s_initialize
        pass

    @staticmethod
    def loadParams(module, param):
        records = DatabaseManager.getDatabaseRecords(module, param)

        if _DEVELOPMENT is True:
            for record in records:
                Param = record.get("Param")

                Debug_Value = record.get("Debug")
                Master_Value = record.get("Master")

                if Debug_Value is None:
                    Trace.log("Manager", 0, "DefaultManager.loadParams invalid setup Value(%s) for Param %s" % ("Debug", Param))
                    return False
                    pass

                if Master_Value is None:
                    Trace.log("Manager", 0, "DefaultManager.loadParams invalid setup Value(%s) for Param %s" % ("Master", Param))
                    return False
                    pass
                pass

        for record in records:
            Param = record.get("Param")
            if _DEVELOPMENT is True:
                Value = record.get("Debug")
                pass
            else:
                Value = record.get("Master")
                pass

            DefaultManager.addDefault(Param, Value)
            pass

        DefaultManager.s_initialize = True

        return True
        pass

    @staticmethod
    def addDefault(name, value):
        DefaultManager.s_defaults[name] = value
        pass

    @staticmethod
    def getDefault(name, default=None):
        if DefaultManager.s_initialize is False:
            Trace.log("Manager", 0, "DefaultManager not initialize")
            return None
            pass

        if name not in DefaultManager.s_defaults:
            return default
            pass

        value = DefaultManager.s_defaults.get(name)

        return value
        pass

    @staticmethod
    def hasDefault(name):
        if DefaultManager.s_initialize is False:
            Trace.log("Manager", 0, "DefaultManager not initialize")
            return False
            pass

        return name in DefaultManager.s_defaults
        pass

    @staticmethod
    def getDefaultKey(name, default=None):
        key = DefaultManager.getDefault(name, default)

        vk_key = Keys.getVirtualKeyCode(key)
        if vk_key is None:
            if default is not None:
                vk_key = Keys.getVirtualKeyCode(default)

        return vk_key

    @staticmethod
    def getDefaultKeyName(name, default=None):
        key = DefaultManager.getDefault(name, default)

        if Keys.getVirtualKeyCode(key) is None:
            if Keys.getVirtualKeyCode(default) is not None:
                key = default.replace("VK_", "")
        else:
            key = key.replace("VK_", "")

        return key

    @staticmethod
    def getDefaultKeyTuple(name, default=None, divider=","):
        b_using_default = False
        values = DefaultManager.getDefault(name)
        if values is None:
            if default is None:
                Trace.log("Manager", 0, "DefaultManager: no values for param {!r} - add default in code or in Default.xlsx".format(name))
                return []
            else:
                values = default
                b_using_default = True

        values = values.split(divider)

        vk_keys = [Keys.getVirtualKeyCode(key) for key in values]
        if None in vk_keys:
            none_indexes = [i for i, key in enumerate(vk_keys) if key is None]

            # check if we not used default value from code before
            if b_using_default is False and default is not None:
                Trace.log("Manager", 0, "DefaultManager: value {!r} from Default.xlsx for {!r} is invalid: {}, try to use default from code {!r}".format(values, name, none_indexes, default))

                # try to use default value because user input from Default.xlsx is invalid
                values = default.split(divider)
                vk_keys = [Keys.getVirtualKeyCode(key) for key in values]

                if None in vk_keys:
                    none_indexes = [i for i, key in enumerate(vk_keys) if key is None]
                    Trace.log("Manager", 0, "DefaultManager: default value {!r} for {!r} from code is invalid too: {}".format(default, name, none_indexes))
                    return []

            else:
                # no other ways except return empty list
                if b_using_default is False:
                    Trace.log("Manager", 0, "DefaultManager: invalid value from Default.xslx ({!r} {}) for {!r}, but no default value from code to fix it".format(values, none_indexes, name))
                else:
                    Trace.log("Manager", 0, "DefaultManager: invalid value {!r} {} for {!r}, but no default value from code to fix it".format(values, none_indexes, name))
                return []

        return vk_keys

    @staticmethod
    def getDefaultBool(name, default):
        value = DefaultManager.getDefault(name, None)

        if value is None:
            return default
            pass

        boolValue = bool(int(value))

        return boolValue
        pass

    @staticmethod
    def getDefaultFloat(name, default):
        value = DefaultManager.getDefault(name, None)

        if value is None:
            return default
            pass

        return float(value)
        pass

    @staticmethod
    def getDefaultInt(name, default):
        value = DefaultManager.getDefault(name, None)

        if value is None:
            return default
            pass

        return int(value)
        pass

    @staticmethod
    def getDefaultTuple(name, default, valueType=float, divider=','):
        value = DefaultManager.getDefault(name, None)

        if value is None:
            return default
            pass

        valuesRaw = value.split(divider)
        # todo: refactor on regular
        # regular = r"\d"
        # values = re.search(regular, value)
        # print 'valuesssssssss', values.groups()
        if valueType:
            values = []
            for valueRaw in valuesRaw:
                try:
                    value = valueType(valueRaw.strip())
                    values.append(value)
                    pass
                except ValueError:
                    Trace.log("Manager", 0, "ERROR: DefaultManager.getDefaultTuple: cannot convert (%s) with type (%s)" % (value, valueType))
                    return default
                pass
            pass
        else:
            values = valuesRaw
            pass

        return tuple(values)
        pass

    @staticmethod
    def removeDefault(name):
        del DefaultManager.s_defaults[name]
        pass