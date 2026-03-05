from Foundation.Manager import Manager
from Foundation.BaseObject import BaseObject
from Foundation.Params import ParamsException

class ObjectManager(Manager):
    s_typesDemain = {}
    s_types = {}

    @staticmethod
    def importObject(module, name, Override=False):
        if Override is True:
            ObjectManager.s_types.pop(name, None)
            ObjectManager.s_typesDemain.pop(name, None)
            pass

        type = "Object%s" % name
        ObjectManager.s_typesDemain[name] = (module, type)

        return True

    @staticmethod
    def __importObjectDemain(module, type):
        try:
            Module = __import__("%s.%s" % (module, type), fromlist=[module])
        except ImportError as ex:
            Trace.log("Manager", 0, "ObjectManager.__importObjectDemain %s:%s error import '%s'\n%s" % (module, type, ex, traceback.format_exc()))

            return None

        try:
            ObjectType = getattr(Module, type)
        except AttributeError as ex:
            Trace.log("Manager", 0, "ObjectManager.__importObjectDemain %s:%s module not found type '%s'\n%s" % (module, type, ex, traceback.format_exc()))

            return None

        try:
            ObjectType.declareORM(ObjectType)
        except ParamsException as pex:
            Trace.log("Manager", 0, "ObjectManager.getObjectType %s:%s type %s params error %s\n%s" % (module, type, ObjectType, pex, traceback.format_exc()))
            return None

        return ObjectType

    @staticmethod
    def getObjectType(name):
        if _DEVELOPMENT is True:
            if name not in ObjectManager.s_typesDemain:
                Trace.log("Manager", 0, "ObjectManager.createObject: not register type %s maybe you forgot add in Pak.xml(Entity) or init in ObjectManager" % (typeName))

                return None

        ObjectType = ObjectManager.s_types.get(name)

        if ObjectType is not None:
            return ObjectType

        module, type = ObjectManager.s_typesDemain[name]

        NewObjectType = ObjectManager.__importObjectDemain(module, type)

        if NewObjectType is None:
            return None

        ObjectManager.s_types[name] = NewObjectType

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
            Trace.log("Manager", 0, "ObjectManager.createObject: Object type %s name %s invalid params" % (typeName, name))
            return None

        return obj

    @staticmethod
    def createObjectUnique(typeName, name, group, **params):
        if _DEVELOPMENT is True:
            if group is not None:
                if issubclass(type(group), BaseObject) is False:
                    Trace.log("Manager", 0, "ObjectManager.createObjectUnique type %s name %s params %s invalid group %s is not subclass BaseObject" % (typeName, name, params, group))

                    return None
                pass
            pass

        obj = ObjectManager.createObject(typeName, name, group, params)

        if obj is None:
            Trace.log("Manager", 0, "ObjectManager.createObjectUnique type %s name %s group %s params %s invalid create" % (typeName, name, group.getName(), params))

            return None

        obj.onInitialize()
        obj.onActivate()
        obj.onEntityRestore()

        obj.setSaving(False)

        return obj
    pass