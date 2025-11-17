from Foundation.Manager import Manager
from Foundation.Object.BaseObject import BaseObject
from Foundation.Params import ParamsException

class ObjectManager(Manager):
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
            Trace.log("Manager", 0, "ObjectManager.__importDemainObject %s:%s error import '%s'\n%s" % (module, type, ex, traceback.format_exc()))

            return None

        try:
            Type = getattr(Module, type)
        except AttributeError as ex:
            Trace.log("Manager", 0, "ObjectManager.__importDemainObject %s:%s module not found type '%s'\n%s" % (module, type, ex, traceback.format_exc()))

            return None

        return Type

    @staticmethod
    def getObjectType(typeName):
        if _DEVELOPMENT is True:
            if typeName not in ObjectManager.s_typesDemain:
                Trace.log("ObjectManager", 0, "ObjectManager.createObject: not register type %s maybe you forgot add in Pak.xml(Entity) or init in ObjectManager" % (typeName))

                return None

        ObjectType = ObjectManager.s_types.get(typeName)

        if ObjectType is not None:
            return ObjectType

        module, type = ObjectManager.s_typesDemain[typeName]

        NewObjectType = ObjectManager.__importDemainObject(module, type)

        if NewObjectType is None:
            return None

        try:
            NewObjectType.declareORM(NewObjectType)
        except ParamsException as pex:
            Trace.log("Manager", 0, "ObjectManager.getObjectType %s:%s params error %s\n%s" % (module, type, pex, traceback.format_exc()))
            return None

        ObjectManager.s_types[typeName] = NewObjectType

        return NewObjectType

    @staticmethod
    def createObject(typeName, name, group, params):
        ObjectType = ObjectManager.getObjectType(typeName)

        if ObjectType is None:
            return None

        obj = ObjectType()

        obj.setEntityType(typeName)
        obj.setName(name)
        obj.setGroup(group)

        if obj.onParams(params) is False:
            Trace.log("ObjectManager", 0, "ObjectManager.createObject: Object %s type %s invalid params" % (name, typeName))
            return None

        return obj

    @staticmethod
    def createObjectUnique(typeName, name, group, **params):
        if _DEVELOPMENT is True:
            if group is not None:
                if issubclass(type(group), BaseObject) is False:
                    Trace.log("ObjectManager", 0, "ObjectManager.createObjectUnique: invalid group %s is not subclass BaseObject" % (group))

                    return None
                pass
            pass

        obj = ObjectManager.createObject(typeName, name, group, params)

        if obj is None:
            Trace.log("ObjectManager", 0, "ObjectManager.createObjectUnique: invalid create")

            return None

        obj.onInitialize()
        obj.onActivate()
        obj.onEntityRestore()

        obj.setSaving(False)

        return obj
    pass