from Foundation.Database import Database


class DatabaseManager(object):
    s_cache_databases = {}
    s_cache_enable = False

    @staticmethod
    def onInitialize():
        DatabaseManager.s_cache_enable = Mengine.getConfigBool("Python", "DatabaseCache", False)

    @staticmethod
    def onFinalize():
        DatabaseManager.s_cache_databases = {}
        DatabaseManager.s_cache_enable = False

    @staticmethod
    def importDatabase(module, name):
        Name = "Database%s" % (name)
        FromName = module
        ModuleName = "%s.%s" % (FromName, Name)

        try:
            Module = __import__(ModuleName, fromlist=[FromName])
        except ImportError as ex:
            Trace.log("Manager", 0, "DatabaseManager.importDatabase: %s:%s invalid import %s" % (module, name, ex))
            return None

        DatabaseType = getattr(Module, Name)
        return DatabaseType

    @staticmethod
    def addExternalDatabaseFromRecords(name, *records):
        if not records:
            return

        database = DatabaseManager.addORMsFromRecords(name, records)
        DatabaseManager.s_cache_databases[name] = database

    @staticmethod
    def addORMsFromRecords(name, records):
        def _record_init(self, record):
            for key, value in record.iteritems():
                setattr(self, key, value)

        RecordType = type("Record{}".format(name), (), dict(__init__=_record_init))
        newDatabase = Database()

        for record in records:
            orm = RecordType(record)
            newDatabase.addORM(orm)

        return newDatabase

    @staticmethod
    def getDatabase(module, name):
        if name in DatabaseManager.s_cache_databases:
            return DatabaseManager.s_cache_databases[name]

        Type = DatabaseManager.importDatabase(module, name)
        if Type is None:
            return None

        Database = Type()

        if DatabaseManager.s_cache_enable is True:
            DatabaseManager.s_cache_databases[name] = Database

        return Database

    @staticmethod
    def getDatabaseRecords(module, param):
        database = DatabaseManager.getDatabase(module, param)

        if database is None:
            Trace.log("Manager", 0, "DatabaseManager.getDatabaseRecords: invalid param %s" % (param))
            return None

        records = database.getRecords()
        return records

    @staticmethod
    def getDatabaseRecordsFilterBy(module, param, **keys):
        records = DatabaseManager.getDatabaseRecords(module, param)

        filter_records = []
        for record in records:
            for key, value in keys.iteritems():
                if record.get(key) == value:
                    filter_records.append(record)

        return filter_records

    @staticmethod
    def getDatabaseORMs(module, param):
        # type: (object, object) -> object
        database = DatabaseManager.getDatabase(module, param)

        if database is None:
            Trace.log("Manager", 0, "DatabaseManager.getDatabaseRecords: invalid param %s" % (param))
            return None

        ORMs = database.getORMs()
        return ORMs

    @staticmethod
    def findDatabaseORM(module, param, **keys):
        ORMs = DatabaseManager.getDatabaseORMs(module, param)
        if ORMs == []:
            return None

        ORM = DatabaseManager.find(ORMs, **keys)
        return ORM

    @staticmethod
    def filterDatabaseORM(module, param, filter):
        ORMs = DatabaseManager.getDatabaseORMs(module, param)
        return [orm for orm in ORMs if filter(orm) is True]

    @staticmethod
    def validDatabaseORMs(param, *legends):
        module = "Database"
        database = DatabaseManager.getDatabase(module, param)

        if database is None:
            Trace.log("Manager", 0, "DatabaseManager.validDatabaseORMs: invalid param %s" % (param))
            return []

        database_legends = database.getLegends()

        successful = True
        for key in database_legends:
            if key not in legends:
                Trace.log("Manager", 0, "DatabaseManager.validDatabaseORMs: database %s has over param %s" % (param, key))
                successful = False

            legends.remove(key)

        for key in legends:
            Trace.log("Manager", 0, "DatabaseManager.validDatabaseORMs: database %s has missing param %s" % (param, key))
            successful = False

        return successful

    @staticmethod
    def getIndexer(orm, master, **keys):
        orm_filter = DatabaseManager.select(orm, **keys)
        indexer = {getattr(v, master): v for v in orm_filter}
        return indexer

    @staticmethod
    def __equal(record, keys):
        for key, value in keys:
            record_key_value = getattr(record, key, None)

            if record_key_value is None:
                if hasattr(record, key) is False:
                    return False

            if record_key_value != value:
                return False

        return True

    @staticmethod
    def find(orm, **keys):
        keys_items = keys.items()

        for record in orm:
            successful = True

            for key, value in keys_items:
                record_key_value = getattr(record, key, None)

                if record_key_value is None:
                    if hasattr(record, key) is False:
                        successful = False
                        break

                if record_key_value != value:
                    successful = False
                    break

                successful = True

            if successful is False:
                continue

            return record

    @staticmethod
    def findDB(db, **keys):
        indexer = db.getIndexer()

        if indexer is None:
            orms = db.getORMs()
            return DatabaseManager.find(orms, **keys)

        elif indexer in keys:
            index = keys[indexer]

            orms = db.selectIndexerORMs(index)
            if orms is None:
                return None

            return DatabaseManager.find(orms, **keys)

        else:
            orms = db.getORMs()
            return DatabaseManager.find(orms, **keys)

    @staticmethod
    def getUniqueORMValues(orm, key):
        unique_values = []
        for record in orm:
            if hasattr(record, key) is False:
                continue

            value = getattr(record, key)
            if value in unique_values:
                continue

            unique_values.append(value)

        return unique_values

    @staticmethod
    def getLowValueFromUniques(orm, key, value):
        unique_values = DatabaseManager.getUniqueORMValues(orm, key)

        low_value = None
        for unique_value in unique_values:
            if low_value is None or unique_value <= value:
                low_value = unique_value

        return low_value

    @staticmethod
    def find_optional(orm, **keys):
        required = {}
        optionals = {}
        for key, value in keys.iteritems():
            if isinstance(value, list) is True:
                optionals[key] = value[0]
            else:
                required[key] = value

        orm_required = DatabaseManager.select(orm, **required)

        if len(orm_required) == 0:
            return None

        orm_optionals = DatabaseManager.find(orm_required, **optionals)

        if orm_optionals is None:
            for record in orm_required:
                for key in optionals:
                    if hasattr(record, key) is False:
                        return record

                    record_value = getattr(record, key)
                    if record_value is None:
                        return record

            return None

        return orm_optionals

    @staticmethod
    def select(orm, **keys):
        keys_items = keys.items()

        result = []
        for record in orm:
            if DatabaseManager.__equal(record, keys_items) is False:
                continue
            result.append(record)

        return result

    @staticmethod
    def unselect(orm, **keys):
        result = []
        for record in orm:
            if DatabaseManager.__equal(record, keys) is True:
                continue
            result.append(record)

        return result

    @staticmethod
    def count(orm, **keys):
        keys_items = keys.items()

        result = 0
        for record in orm:
            if DatabaseManager.__equal(record, keys_items) is False:
                continue
            result += 1

        return result

    @staticmethod
    def exist(orm, **keys):
        keys_items = keys.items()

        for record in orm:
            if DatabaseManager.__equal(record, keys_items) is False:
                continue
            return True

        return False

    @staticmethod
    def getValueFromEntityDefaults(key, entity, tag=None):
        entityDefaultORMs = DatabaseManager.getDatabaseORMs('Database', 'EntityDefaults')
        defaultORMs = DatabaseManager.select(entityDefaultORMs, Entity=entity)
        if tag is None:
            value = DatabaseManager.find(defaultORMs, Entity=entity, Key=key).Value
        else:
            value = DatabaseManager.find(defaultORMs, Entity=entity, Key=key, Tag=tag).Value

        return value
