from Foundation.Manager import Manager
from Foundation.Params import ParamsException

class EntityManager(Manager):
    s_type = {}
    s_typeDemain = {}

    @staticmethod
    def importEntity(module, name, override=False):
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

        EntityManager.s_type[name] = (module, name)

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
        EntityManager.s_type = {}
        pass