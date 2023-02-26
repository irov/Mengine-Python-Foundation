import Trace
from GOAP2.Object.BaseObject import BaseObject

class ObjectManager(object):
    s_typesDemain = {}
    s_types = {}

    @staticmethod
    def importObjects(module, prototypes):
        for prototype in prototypes:
            if ObjectManager.importObject(module, prototype) is False:
                return False
        return True

    @staticmethod
    def importObject(module, prototype):
        if isinstance(prototype, dict):
            name = prototype['name']
        else:
            name = prototype

        type = "Object%s" % name
        module_pure = "%s" % module
        ObjectManager.s_typesDemain[name] = (module_pure, type)

        return True
        pass

    @staticmethod
    def __importDemainObject(module, type):
        if module == "":
            ModuleName = type
        else:
            ModuleName = "%s.%s" % (module, type)

        try:
            if module == "":
                Module = __import__(ModuleName)
            else:
                Module = __import__(ModuleName, fromlist=[module])
                pass
        except ImportError as ex:
            traceback.print_exc()

            Trace.log("Manager", 0, "ObjectManager.__importDemainObject %s:%s error import '%s'" % (module, type, ex))

            return None
            pass

        try:
            Type = getattr(Module, type)
        except AttributeError as ex:
            traceback.print_exc()

            Trace.log("Manager", 0, "ObjectManager.__importDemainObject %s:%s module not found type '%s'" % (module, type, ex))

            return None
            pass

        return Type
        pass

    @staticmethod
    def getObjectType(typeName):
        if typeName not in ObjectManager.s_typesDemain:
            Trace.log("ObjectManager", 0, "ObjectManager.createObject: not register type %s maybe you forgot add in Pak.xml(Entity) or init in ObjectManager" % (typeName))

            return None
            pass

        ObjectType = ObjectManager.s_types.get(typeName)

        if ObjectType is None:
            module, type = ObjectManager.s_typesDemain[typeName]

            ObjectType = ObjectManager.__importDemainObject(module, type)

            if ObjectType is None:
                return None
                pass

            ObjectType.declareORM(ObjectType)

            ObjectManager.s_types[typeName] = ObjectType

        return ObjectType
        pass

    @staticmethod
    def createObject(typeName, name, group, params):
        ObjectType = ObjectManager.getObjectType(typeName)

        if ObjectType is None:
            return None
            pass

        obj = ObjectType()

        obj.setEntityType(typeName)
        obj.setName(name)
        obj.setGroup(group)

        if obj.onParams(params) is False:
            Trace.log("ObjectManager", 0, "ObjectManager.createObject: Object %s type %s invalid params" % (name, typeName))
            return None
            pass

        return obj
        pass

    @staticmethod
    def createObjectUnique(typeName, name, group, **params):
        if _DEVELOPMENT is True:
            if group is not None:
                if issubclass(type(group), BaseObject) is False:
                    Trace.log("ObjectManager", 0, "ObjectManager.createObjectUnique: invalid group %s is not subclass BaseObject" % (group))

                    return None
                    pass
                pass
            pass

        obj = ObjectManager.createObject(typeName, name, group, params)

        if obj is None:
            Trace.log("ObjectManager", 0, "ObjectManager.createObjectUnique: invalid create")

            return None
            pass

        obj.onInitialize()
        obj.onActivate()
        obj.onEntityRestore()

        obj.setSaving(False)

        return obj
        pass
    pass