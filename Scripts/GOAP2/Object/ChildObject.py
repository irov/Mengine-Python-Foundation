from GOAP2.Object.BaseObject import BaseObject

from GOAP2.Object.ObjectCollection import ObjectCollection
from GOAP2.ObjectManager import ObjectManager

class ChildObject(BaseObject):
    def __init__(self):
        super(ChildObject, self).__init__()

        self.child = ObjectCollection()
        self.child_unique = ObjectCollection()

        self.prototypes = {}

        self.currentLayerName = None
        pass

    def setCurrentLayerName(self, name):
        self.currentLayerName = name
        pass

    def addPrototype(self, Type, Name, Preparation=None, **Params):
        Prototype = (Type, Preparation, Params, self.currentLayerName)

        self.prototypes[Name] = Prototype
        pass

    def getPrototype(self, prototypeName):
        if prototypeName not in self.prototypes:
            return None
            pass

        return self.prototypes[prototypeName]
        pass

    def hasPrototype(self, prototypeName):
        return prototypeName in self.prototypes
        pass

    def generateObject(self, objectName, prototypeName, prototypeParams=None):
        if self.hasObject(objectName) is True:
            Trace.log("Object", 0, "ChildObject.generateObject: %s prototype [%s] already has [%s]" % (self.getName(), prototypeName, objectName))
            return None
            pass

        if self.isActive() is False:
            Trace.log("Object", 0, "ChildObject.generateObject: %s inactivate [%s]" % (self.getName(), prototypeName))
            return None
            pass

        Prototype = self.getPrototype(prototypeName)

        if Prototype is None:
            Trace.log("Object", 0, "ChildObject.generateObject: %s unknown prototype [%s]" % (self.getName(), prototypeName))
            return None
            pass

        PrototypeType, PrototypePreparation, PrototypeParams, PrototypeLayerName = Prototype

        params = PrototypeParams.copy()

        if isinstance(prototypeParams, dict) is True:
            params.update(prototypeParams)
            pass
        elif prototypeParams is not None:
            Trace.log("Object", 0, "ChildObject.generateObject: %s must be instance of dictinary" % (prototypeParams,))
            pass

        obj = ObjectManager.createObject(PrototypeType, objectName, self, params)

        obj.setPrototypeName(prototypeName)
        obj.setLayerName(PrototypeLayerName)

        if PrototypePreparation is not None:
            PrototypePreparation(obj)
            pass

        if self._addObject(objectName, obj) is False:
            return None
            pass

        obj.onInitialize()
        obj.onActivate()
        obj.onEntityRestore()

        obj.setSaving(False)

        entity = obj.getEntity()
        self.entity.addChild(entity.node)

        return obj
        pass

    def tryGenerateObject(self, objectName, prototypeName, prototypeParams=None):
        if self.hasPrototype(prototypeName) is False:
            return None
            pass

        return self.generateObject(objectName, prototypeName, prototypeParams)
        pass

    def generateObjectUnique(self, objectName, prototypeName, **prototypeParams):
        Prototype = self.getPrototype(prototypeName)

        if Prototype is None:
            Trace.log("Object", 0, "ChildObject.generateObject: %s unknown prototype [%s]" % (self.getName(), prototypeName))
            return None
            pass

        PrototypeType, PrototypePreparation, PrototypeParams, PrototypeLayerName = Prototype

        params = PrototypeParams.copy()
        params.update(prototypeParams)
        params.setdefault("Enable", False)

        obj = ObjectManager.createObject(PrototypeType, objectName, self, params)

        obj.setPrototypeName(prototypeName)
        obj.setLayerName(PrototypeLayerName)

        if PrototypePreparation is not None:
            PrototypePreparation(obj)
            pass

        if self._addObjectUnique(objectName, obj) is False:
            return None
            pass

        obj.onInitialize()
        obj.onActivate()
        obj.onEntityRestore()

        obj.setSaving(False)

        return obj
        pass

    def tryGenerateObjectUnique(self, objectName, prototypeName, **prototypeParams):
        if self.hasPrototype(prototypeName) is False:
            return None
            pass

        return self.generateObjectUnique(objectName, prototypeName, **prototypeParams)
        pass

    def onLoader(self):
        super(ChildObject, self).onLoader()

        objects = self.getObjects()
        for obj in objects[:]:
            if obj.isSaving() is False:
                obj.onDestroy()
                pass
            else:
                obj.onLoader()
                pass
            pass
        pass

    def createObject(self, Type, Name, **Params):
        if self.hasObject(Name) is True:
            if self.loaded is False:
                Trace.log("Object", 0, "ChildObject '%s' already exist child '%s'" % (self.name, Name))
                return None
                pass

            obj = self.getObject(Name)
            obj.onReloadParams(Params)

            return obj
            pass

        obj = ObjectManager.createObject(Type, Name, self, Params)

        if obj is None:
            Trace.log("Object", 0, "ChildObject '%s' invalid create child '%s:%s'" % (self.name, Type, Name))

            return None
            pass

        obj.setLayerName(self.currentLayerName)

        if self._addObject(Name, obj) is False:
            return None
            pass

        return obj
        pass

    def addObject(self, obj):
        name = obj.getName()

        if self._addObject(name, obj) is False:
            return
            pass

        if obj.isInitialized() is False:
            if obj.onInitialize() is False:
                Trace.log("Object", 0, "ChildObject '%s' invalid initialize '%s'" % (self.name, name))
                pass
            pass

        if obj.isActive() is False:
            if obj.onActivate() is False:
                Trace.log("Object", 0, "ChildObject '%s' invalid activate '%s'" % (self.name, name))
                pass
            pass

        obj_entityNode = obj.getEntityNode()
        self.entity.addChild(obj_entityNode)
        pass

    def _addObject(self, name, obj):
        if self.hasObject(name) is True:
            Trace.log("Object", 0, "ChildObject._addObject '%s' already exist child '%s'" % (self.name, name))

            return False
            pass

        parent = obj.getParent()
        if parent is not None:
            obj.removeFromParent()
            pass

        obj.setParent(self)
        obj.setGroup(self)

        self.child.append(name, obj)

        return True
        pass

    def _addObjectUnique(self, name, obj):
        parent = obj.getParent()
        if parent is not None:
            obj.removeFromParent()
            pass

        obj.setGroup(self)

        self.child_unique.append(name, obj)

        return True
        pass

    def removeObject(self, name):
        if self.hasObject(name) is False:
            Trace.log("Object", 0, "ChildObject.removeObject '%s' invalid remove child '%s' don't found" % (self.name, name))
            return
            pass

        obj = self.getObject(name)
        obj.setParent(None)
        #        obj.setGroup(None)

        self.child.remove(name)
        pass

    def getObject(self, name):
        obj = self.child.get(name)

        if obj is None:
            GroupName = self.getGroupName()
            Trace.log("Object", 0, "ChildObject '%s:%s' not found child '%s'" % (GroupName, self.name, name))

            return None
            pass

        return obj
        pass

    def hasObject(self, name):
        return name in self.child
        pass

    def tryObject(self, name):
        obj = self.child.get(name)

        return obj
        pass

    def getObjects(self):
        return self.child.getList()
        pass

    def visitObjects(self, cb):
        cb(self)

        self.visitChild(cb)
        pass

    def visitObjects2(self, cb):
        if cb(self) is False:
            return False
            pass

        for child in self.child + self.child_unique:
            if child.visitObjects(cb) is False:
                return False
                pass
            pass

        return True
        pass

    def visitObjectsBrakeOnFalse(self, cb):
        if cb(self) is False:
            return False

        for child in self.child + self.child_unique:
            if child.visitObjects2(cb) is False:
                return False

        return True

    def visitChild(self, cb):
        for child in self.child + self.child_unique:
            child.visitObjects(cb)
            pass
        pass

    def _onInitialize(self):
        super(ChildObject, self)._onInitialize()

        objects = self.getObjects()

        for obj in objects:
            if obj.onInitialize() is False:
                self.initializeFailed("child %s invalid initialize" % (obj.getName))
                pass
            pass
        pass

    def _onFinalize(self):
        super(ChildObject, self)._onFinalize()

        objects = self.getObjects()

        for obj in objects:
            obj.onFinalize()
            pass
        pass

    def _onDeactivate(self):
        super(ChildObject, self)._onDeactivate()

        objects = self.getObjects()

        for obj in objects:
            obj.onDeactivate()
            pass
        pass

    def _onDestroy(self):
        super(ChildObject, self)._onDestroy()

        objects = self.getObjects()

        for obj in objects[:]:
            obj.onDestroy()
            pass

        self.child = None
        pass
    pass