from Foundation.Manager import Manager
from Foundation.Params import ParamsException

class EntityManager(Manager):
    s_types = {}
    s_typesDemain = {}

    @staticmethod
    def importEntity(module, name, Override=False):
        if Override is True:
            if Mengine.hasEntityPrototypeFinder(name) is True:
                Mengine.removeEntityPrototypeFinder(name)

        if _DEVELOPMENT is True and Override is False:
            if name in EntityManager.s_types:
                module2, typeName2 = EntityManager.s_types[name]

                Trace.log("Manager", 0, "EntityManager.importEntity module %s name %s already exist (old_module '%s' old_name '%s')" % (module, name, module2, typeName2))
                return False

        if Mengine.addEntityPrototypeFinder(name, EntityManager.__importEntityType) is False:
            Trace.log("Manager", 0, "EntityManager.importEntity invalid add module %s name %s" % (module, name))

            return False

        EntityManager.s_types[name] = (module, name)

        return True

    @staticmethod
    def __importEntityType(name):
        module, type = EntityManager.s_types[name]

        EntityType = EntityManager.__importEntityDemain(module, type)

        if EntityType is None:
            return None

        return EntityType

    @staticmethod
    def __importEntityDemain(module, type):
        try:
            Module = __import__("%s.%s" % (module, type), fromlist=[module])

        except ImportError as se:
            Trace.log("Manager", 0, "EntityManager.__importEntityDemain %s:%s import error %s\n%s" % (module, type, se, traceback.format_exc()))
            return None

        try:
            EntityType = getattr(Module, type)
        except AttributeError as ex:
            Trace.log("Manager", 0, "EntityManager.__importEntityDemain %s:%s module not found type '%s'\n%s" % (module, type, ex, traceback.format_exc()))
            return None

        try:
            EntityType.declareORM(EntityType)
        except ParamsException as pex:
            Trace.log("Manager", 0, "EntityManager.__importEntityDemain %s:%s params error %s\n%s" % (module, type, pex, traceback.format_exc()))
            return None

        return EntityType

    @staticmethod
    def _onInitialize():
        pass

    @staticmethod
    def _onFinalize():
        EntityManager.s_types = {}
        pass