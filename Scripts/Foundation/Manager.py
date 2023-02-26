class Manager(object):
    s__observers = []

    @classmethod
    def onInitialize(cls, *args):
        if cls._onSave is not Manager._onSave:
            cls.addObserver(Notificator.onSessionSave, cls.__onSessionSave)
            pass

        if cls._onLoad is not Manager._onLoad:
            cls.addObserver(Notificator.onSessionLoad, cls.__onSessionLoad)
            pass

        cls._onInitialize(*args)

        return True
        pass

    @classmethod
    def _onInitialize(cls, *args):
        pass

    @classmethod
    def onFinalize(cls):
        for observer in cls.s__observers:
            Notification.removeObserver(observer)
            pass

        cls.s__observers = []

        cls._onFinalize()
        pass

    @classmethod
    def _onFinalize(cls):
        pass

    @classmethod
    def __onSessionSave(cls, dict_global):
        dict_save = cls._onSave()

        if dict_save is None:
            Trace.log("Manager", 0, "Manager.__onSessionSave %s save return 'None'" % (cls))

            return False
            pass

        dict_global.setdefault("Manager", {})
        dict_global["Manager"][cls.__name__] = dict_save

        return False
        pass

    @classmethod
    def _onSave(cls):
        return {}
        pass

    @classmethod
    def __onSessionLoad(cls, dict_global):
        dict_save = dict_global.get("Manager", {}).get(cls.__name__, {})

        try:
            cls._onLoad(dict_save)
        except Exception as ex:
            traceback.print_exc()

            Trace.log("Manager", 0, "Manager.__onSessionLoad %s invalid load" % (cls))

            Menge.changeCurrentAccountSetting("InvalidLoad", u"True")

        return False
        pass

    @classmethod
    def _onLoad(cls, dict_save):
        pass

    @classmethod
    def addObserver(cls, ID, Function, *Args, **Kwds):
        observer = Notification.addObserver(ID, Function, *Args, **Kwds)

        if observer is None:
            return
            pass

        cls.s__observers.append(observer)

    @staticmethod
    def loadParams(module, name):
        """
            loads database, all params auto-injected by Bootstrapper.

            Usage example:

            >>> from Foundation.DatabaseManager import DatabaseManager
            >>>
            >>> s_data = {}
            >>>
            >>> records = DatabaseManager.getDatabaseRecords(module, name)
            >>> for record in records:
            >>>     key = record.get("Key", "DefaultKey")
            >>>     value = record.get("Value", -1)
            >>>     s_data[key] = value

            @param module: 'Database' as usual.
            @param name: name of database without module prefix.
        """
        pass

    @staticmethod
    def getRecordValue(record, key, cast=None, default=None):
        """ Util for loadParams, that helps in records loading

            :returns: value from `record` with given `key`
            :param cast: type in which value will be cast
            :param default: default value if given value not exist in record

            Usage example:

            >>> class Param(object):
            >>>     def __init__(self, record: dict):
            >>>         self.descr = Manager.getRecordValue(record, "DescrTextID", default="ID_EMPTY")
            >>>         self.title = Manager.getRecordValue(record, "TitleTextID", default="ID_EMPTY")
            >>>         ...
            >>> ...
            >>> records = {...}
            >>> for record in records:
            >>>     params = Param(record)  # one line - all params gathered
        """

        value = record.get(key, default)

        if callable(cast) is True and value is not None:
            if cast == list:
                value = value.split(", ")
            else:
                value = cast(value)

        return value