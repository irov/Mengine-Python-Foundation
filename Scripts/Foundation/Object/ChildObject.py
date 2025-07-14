from Foundation.Object.BaseObject import BaseObject
from Foundation.Object.ObjectCollection import ObjectCollection
from Foundation.ObjectManager import ObjectManager


class ChildObject(BaseObject):
    def __init__(self):
        super(ChildObject, self).__init__()

        self.child = ObjectCollection()
        self.child_unique = ObjectCollection()

        self.prototypes = {}

        self.currentLayerName = None

    def setCurrentLayerName(self, name):
        self.currentLayerName = name

    def addPrototype(self, Type, Name, Preparation=None, **Params):
        Prototype = (Type, Preparation, Params, self.currentLayerName)

        self.prototypes[Name] = Prototype

    def getPrototype(self, prototypeName):
        if prototypeName not in self.prototypes:
            return None

        return self.prototypes[prototypeName]

    def hasPrototype(self, prototypeName):
        return prototypeName in self.prototypes

    def generateObject(self, objectName, prototypeName, prototypeParams=None):
        if self.hasObject(objectName) is True:
            Trace.log("Object", 0, "ChildObject.generateObject: %s prototype [%s] already has [%s]" % (self.getName(), prototypeName, objectName))
            return None

        if self.isActive() is False:
            Trace.log("Object", 0, "ChildObject.generateObject: %s inactivate [%s]" % (self.getName(), prototypeName))
            return None

        Prototype = self.getPrototype(prototypeName)

        if Prototype is None:
            Trace.log("Object", 0, "ChildObject.generateObject: %s unknown prototype [%s]" % (self.getName(), prototypeName))
            return None

        PrototypeType, PrototypePreparation, PrototypeParams, PrototypeLayerName = Prototype

        params = PrototypeParams.copy()

        if isinstance(prototypeParams, dict) is True:
            params.update(prototypeParams)
        elif prototypeParams is not None:
            Trace.log("Object", 0, "ChildObject.generateObject: %s must be instance of dictionary" % (prototypeParams,))

        obj = ObjectManager.createObject(PrototypeType, objectName, self, params)

        obj.setPrototypeName(prototypeName)
        obj.setLayerName(PrototypeLayerName)

        if PrototypePreparation is not None:
            PrototypePreparation(obj)

        if self._addObject(objectName, obj) is False:
            return None

        obj.onInitialize()
        obj.onActivate()
        obj.onEntityRestore()

        obj.setSaving(False)

        obj_entityNode = obj.getEntityNode()
        self.entity.addChild(obj_entityNode)

        return obj

    def tryGenerateObject(self, objectName, prototypeName, prototypeParams=None):
        if self.hasPrototype(prototypeName) is False:
            return None

        return self.generateObject(objectName, prototypeName, prototypeParams)

    def generateObjectUnique(self, objectName, prototypeName, **prototypeParams):
        Prototype = self.getPrototype(prototypeName)

        if Prototype is None:
            Trace.log("Object", 0, "ChildObject.generateObject: %s unknown prototype [%s]" % (self.getName(), prototypeName))
            return None

        PrototypeType, PrototypePreparation, PrototypeParams, PrototypeLayerName = Prototype

        params = PrototypeParams.copy()
        params.update(prototypeParams)
        params.setdefault("Enable", False)

        obj = ObjectManager.createObject(PrototypeType, objectName, self, params)

        obj.setPrototypeName(prototypeName)
        obj.setLayerName(PrototypeLayerName)

        if PrototypePreparation is not None:
            PrototypePreparation(obj)

        if self._addObjectUnique(objectName, obj) is False:
            return None

        obj.onInitialize()
        obj.onActivate()
        obj.onEntityRestore()

        obj.setSaving(False)

        obj_entityNode = obj.getEntityNode()
        self.entity.addChild(obj_entityNode)

        return obj

    def tryGenerateObjectUnique(self, objectName, prototypeName, **prototypeParams):
        if self.hasPrototype(prototypeName) is False:
            return None

        return self.generateObjectUnique(objectName, prototypeName, **prototypeParams)

    def onLoader(self):
        super(ChildObject, self).onLoader()

        objects = self.getObjects()
        for obj in objects[:]:
            if obj.isSaving() is False:
                obj.onDestroy()
            else:
                obj.onLoader()

    def createObject(self, Type, Name, **Params):
        if self.hasObject(Name) is True:
            if self.loaded is False:
                Trace.log("Object", 0, "ChildObject '%s' already exist child '%s'"%(self.name, Name))
                return None

            obj = self.getObject(Name)
            obj.onReloadParams(Params)

            return obj

        obj = ObjectManager.createObject(Type, Name, self, Params)

        if obj is None:
            Trace.log("Object", 0, "ChildObject '%s' invalid create child '%s:%s'"%(self.name, Type, Name))

            return None

        obj.setLayerName(self.currentLayerName)

        if self._addObject(Name, obj) is False:
            return None

        return obj

    def addObject(self, obj):
        name = obj.getName()

        if self._addObject(name, obj) is False:
            return

        if obj.isInitialized() is False:
            if obj.onInitialize() is False:
                Trace.log("Object", 0, "ChildObject '%s' invalid initialize '%s'" % (self.name, name))

        if obj.isActive() is False:
            if obj.onActivate() is False:
                Trace.log("Object", 0, "ChildObject '%s' invalid activate '%s'" % (self.name, name))

        obj_entityNode = obj.getEntityNode()
        self.entity.addChild(obj_entityNode)

    def _addObject(self, name, obj):
        if self.hasObject(name) is True:
            Trace.log("Object", 0, "ChildObject._addObject '%s' already exist child '%s'" % (self.name, name))

            return False

        parent = obj.getParent()
        if parent is not None:
            obj.removeFromParent()

        obj.setParent(self)
        obj.setGroup(self)

        self.child.append(name, obj)

        return True

    def _addObjectUnique(self, name, obj):
        parent = obj.getParent()
        if parent is not None:
            obj.removeFromParent()

        obj.setGroup(self)

        self.child_unique.append(name, obj)

        return True

    def removeObject(self, name):
        if self.hasObject(name) is False:
            Trace.log("Object", 0, "ChildObject.removeObject '%s' invalid remove child '%s' don't found" % (self.name, name))
            return

        obj = self.getObject(name)
        obj.setParent(None)
        #        obj.setGroup(None)

        self.child.remove(name)

    def getObject(self, name):
        obj = self.child.get(name)

        if obj is None:
            GroupName = self.getGroupName()
            Trace.log("Object", 0, "ChildObject '%s:%s' not found child '%s'" % (GroupName, self.name, name))

            return None

        return obj

    def hasObject(self, name):
        return name in self.child

    def tryObject(self, name):
        obj = self.child.get(name)

        return obj

    def getObjects(self):
        return self.child.getList()

    def visitObjects(self, cb):
        cb(self)

        self.visitChild(cb)

    def visitObjects2(self, cb):
        if cb(self) is False:
            return False

        for child in self.child + self.child_unique:
            if child.visitObjects(cb) is False:
                return False

        return True

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

    def _onInitialize(self):
        super(ChildObject, self)._onInitialize()

        objects = self.getObjects()

        for obj in objects:
            if obj.onInitialize() is False:
                self.initializeFailed("child %s invalid initialize" % obj.getName())

    def _onFinalize(self):
        super(ChildObject, self)._onFinalize()

        objects = self.getObjects()

        for obj in objects:
            obj.onFinalize()

    def _onDeactivate(self):
        super(ChildObject, self)._onDeactivate()

        objects = self.getObjects()

        for obj in objects:
            obj.onDeactivate()

    def _onDestroy(self):
        super(ChildObject, self)._onDestroy()

        objects = self.getObjects()

        for obj in objects[:]:
            obj.onDestroy()

        self.child = None
