from Foundation.Params import ParamsException

class EntityManager(object):
    s_type = {}
    s_typeDemain = {}

    @staticmethod
    def importEntities(module, prototypes):
        for prototype in prototypes:
            if EntityManager.importEntity(module, prototype) is False:
                return False
        return True

    @staticmethod
    def importEntity(module, prototype):
        if isinstance(prototype, dict):
            name = prototype.get("name")
            type = prototype.get("name")
            override = prototype.get("override", False)
        else:
            name = prototype
            type = prototype
            override = False

        module = "%s.%s" % (module, name)

        if override is True:
            if Mengine.hasEntityPrototypeFinder(name) is True:
                Mengine.removeEntityPrototypeFinder(name)

        if Mengine.addEntityPrototypeFinder(name, EntityManager.__importEntityType) is False:
            if name in EntityManager.s_type:
                module2, type2 = EntityManager.s_type[name]

                Trace.log("Manager", 0, "EntityManager.importEntity entity %s module %s type %s already exist (module '%s' type '%s')" % (name, module, type, module2, type2))
            else:
                Trace.log("Manager", 0, "EntityManager.importEntity invalid add entity %s module %s type %s" % (name, module, type))

            return False

        EntityManager.s_type[name] = (module, type)

        return True

    @staticmethod
    def __importEntityType(name):
        module, type = EntityManager.s_type[name]

        EntityType = EntityManager.__importEntityDemain(module, type)

        if EntityType is None:
            return None

        return EntityType

    @staticmethod
    def __importEntityDemain(module, type):
        if module == "":
            ModuleName = type
        else:
            ModuleName = "%s.%s" % (module, type)

        try:
            if module == "":
                Module = __import__(ModuleName)
            else:
                Module = __import__(ModuleName, fromlist=[module])

        except ImportError as se:
            traceback.print_exc()

            Trace.log("Manager", 0, "EntityManager.__importEntityDemain %s:%s import error %s" % (module, type, se))
            return None

        try:
            Type = getattr(Module, type)
        except AttributeError as ex:
            traceback.print_exc()

            Trace.log("Manager", 0, "EntityManager.__importEntityDemain %s:%s module not found type '%s'" % (module, type, ex))
            return None

        try:
            Type.declareORM(Type)
        except ParamsException as pe:
            traceback.print_exc()

            Trace.log("Manager", 0, "EntityManager.__importEntityDemain %s:%s params error %s" % (module, type, pe))
            return None

        return Type

    @staticmethod
    def onInitialize():
        pass

    @staticmethod
    def onFinalize():
        EntityManager.s_type = {}