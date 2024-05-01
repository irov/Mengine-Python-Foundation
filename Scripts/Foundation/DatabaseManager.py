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
        """ returns database that matches given module:name """
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
    def getDatabaseRecords(module, name):
        """ returns list of database records of given db """
        database = DatabaseManager.getDatabase(module, name)

        if database is None:
            Trace.log("Manager", 0, "DatabaseManager.getDatabaseRecords: module %s invalid name %s" % (module, name))
            return None

        records = database.getRecords()
        return records

    @staticmethod
    def getDatabaseRecordsFilterBy(module, name, **keys):
        """ returns list of database records of given db that match given keys """
        records = DatabaseManager.getDatabaseRecords(module, name)

        filter_records = []
        for record in records:
            for key, value in keys.iteritems():
                if record.get(key) == value:
                    filter_records.append(record)

        return filter_records

    @staticmethod
    def getDatabaseORMs(module, name):
        """ returns the list of ORM, module='Database' as usual """
        database = DatabaseManager.getDatabase(module, name)

        if database is None:
            Trace.log("Manager", 0, "DatabaseManager.getDatabaseRecords: module %s invalid name %s" % (module, name))
            return None

        ORMs = database.getORMs()
        return ORMs

    @staticmethod
    def findDatabaseORM(module, name, **keys):
        """ returns the first ORM that matches the keys if exists in given db """
        ORMs = DatabaseManager.getDatabaseORMs(module, name)
        if ORMs == []:
            return None

        ORM = DatabaseManager.find(ORMs, **keys)
        return ORM

    @staticmethod
    def filterDatabaseORM(module, name, filter):
        """ returns the list of ORM that match the filter """
        ORMs = DatabaseManager.getDatabaseORMs(module, name)
        return [orm for orm in ORMs if filter(orm) is True]

    @staticmethod
    def validDatabaseORMs(name, *legends):
        module = "Database"
        database = DatabaseManager.getDatabase(module, name)

        if database is None:
            Trace.log("Manager", 0, "DatabaseManager.validDatabaseORMs: module %s invalid name %s" % (module, name))
            return []

        database_legends = database.getLegends()

        successful = True
        for key in database_legends:
            if key not in legends:
                Trace.log("Manager", 0, "DatabaseManager.validDatabaseORMs: database %s has over name %s" % (name, key))
                successful = False

            legends.remove(key)

        for key in legends:
            Trace.log("Manager", 0, "DatabaseManager.validDatabaseORMs: database %s has missing name %s" % (name, key))
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
        """ returns the first ORM record that matches the keys """
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
        """ returns list of records with unique values for the given key """
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
        """ returns the lowest unique value for the given key """
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
        """ returns list of all records that match the keys """
        keys_items = keys.items()

        result = []
        for record in orm:
            if DatabaseManager.__equal(record, keys_items) is False:
                continue
            result.append(record)

        return result

    @staticmethod
    def selectByLowBound(orm, key, value):
        """ returns list of orms that have closest and lowest own key value to `value` """
        closest_value = DatabaseManager.getLowValueFromUniques(orm, key, value)
        return DatabaseManager.select(orm, **{key: closest_value})

    @staticmethod
    def unselect(orm, **keys):
        """ returns list of all records that DON'T match the keys """
        result = []
        for record in orm:
            if DatabaseManager.__equal(record, keys) is True:
                continue
            result.append(record)

        return result

    @staticmethod
    def count(orm, **keys):
        """ returns int that represents the number of records that match the keys """
        keys_items = keys.items()

        result = 0
        for record in orm:
            if DatabaseManager.__equal(record, keys_items) is False:
                continue
            result += 1

        return result

    @staticmethod
    def exist(orm, **keys):
        """ returns True if there is at least one record that matches the keys """
        keys_items = keys.items()

        for record in orm:
            if DatabaseManager.__equal(record, keys_items) is False:
                continue
            return True

        return False

    @staticmethod
    def getValueFromEntityDefaults(key, entity, tag=None):
        """ returns ORM's `Value` from db 'EntityDefaults' that matches Entity=entity, Key=key and Tag=tag if given """
        entityDefaultORMs = DatabaseManager.getDatabaseORMs('Database', 'EntityDefaults')
        defaultORMs = DatabaseManager.select(entityDefaultORMs, Entity=entity)
        if tag is None:
            value = DatabaseManager.find(defaultORMs, Entity=entity, Key=key).Value
        else:
            value = DatabaseManager.find(defaultORMs, Entity=entity, Key=key, Tag=tag).Value

        return value
