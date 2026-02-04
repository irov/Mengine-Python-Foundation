from Foundation.Object.BaseObject import BaseObject
from Foundation.Object.ObjectCollection import ObjectCollection
from Foundation.ObjectManager import ObjectManager


class ChildObject(BaseObject):
    def __init__(self):
        super(ChildObject, self).__init__()

        self.child = ObjectCollection()
        self.child_unique = []

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

        return self.prototypes[prototypeName]

    def hasPrototype(self, prototypeName):
        return prototypeName in self.prototypes

    def generateObject(self, objectName, prototypeName, prototypeParams=None, EntityHierarchy=True):
        if _DEVELOPMENT is True and self.hasObject(objectName) is True:
            Trace.log("Object", 0, "ChildObject.generateObject: %s prototype [%s] already has [%s]" % (self.getName(), prototypeName, objectName))
            return None

        if self.isActive() is False:
            Trace.log("Object", 0, "ChildObject.generateObject: %s inactivate [%s]" % (self.getName(), prototypeName))
            return None

        Prototype = self.getPrototype(prototypeName)

        if Prototype is None:
            Trace.log("Object", 0, "ChildObject.generateObject: %s unknown prototype [%s]" % (self.getName(), prototypeName))
            return None

        PrototypeTypeName, PrototypePreparation, PrototypeParams, PrototypeLayerName = Prototype

        params = PrototypeParams.copy()

        if isinstance(prototypeParams, dict) is True:
            params.update(prototypeParams)
        elif prototypeParams is not None:
            Trace.log("Object", 0, "ChildObject.generateObject: %s must be instance of dictionary" % (prototypeParams,))
            pass

        obj = ObjectManager.createObject(PrototypeTypeName, objectName, self, params)

        obj.setLayerName(PrototypeLayerName)

        if PrototypePreparation is not None:
            PrototypePreparation(obj)

        if self._addObject(objectName, obj) is False:
            return None

        obj.onInitialize()
        obj.onActivate()
        obj.onEntityRestore()

        obj.setSaving(False)
        obj.setUnique(False)

        if EntityHierarchy is True:
            obj_entityNode = obj.getEntityNode()
            self.entity.addChild(obj_entityNode)
            pass

        return obj

    def tryGenerateObject(self, objectName, prototypeName, prototypeParams=None, EntityHierarchy=True):
        if self.hasPrototype(prototypeName) is False:
            return None

        return self.generateObject(objectName, prototypeName, prototypeParams, EntityHierarchy=EntityHierarchy)

    def generateObjectUnique(self, objectName, prototypeName, EntityHierarchy=True, **prototypeParams):
        Prototype = self.getPrototype(prototypeName)

        if Prototype is None:
            Trace.log("Object", 0, "ChildObject.generateObject: %s unknown prototype [%s]" % (self.getName(), prototypeName))
            return None

        PrototypeTypeName, PrototypePreparation, PrototypeParams, PrototypeLayerName = Prototype

        params = PrototypeParams.copy()
        params.update(prototypeParams)
        params.setdefault("Enable", False)

        obj = ObjectManager.createObject(PrototypeTypeName, objectName, self, params)

        obj.setLayerName(PrototypeLayerName)

        if PrototypePreparation is not None:
            PrototypePreparation(obj)

        if self._addObjectUnique(obj) is False:
            return None

        obj.onInitialize()
        obj.onActivate()
        obj.onEntityRestore()

        obj.setSaving(False)
        obj.setUnique(True)

        if EntityHierarchy is True:
            obj_entityNode = obj.getEntityNode()
            self.entity.addChild(obj_entityNode)
            pass

        return obj

    def generateNodeUnique(self, prototypeName):
        Prototype = self.getPrototype(prototypeName)

        if Prototype is None:
            Trace.log("Object", 0, "ChildObject.generateNodeUnique: %s unknown prototype [%s]" % (self.getName(), prototypeName))
            return None

        PrototypeTypeName, PrototypePreparation, PrototypeParams, PrototypeLayerName = Prototype

        PrototypeType = ObjectManager.getObjectType(PrototypeTypeName)

        if PrototypeType is None:
            Trace.log("Object", 0, "ChildObject.generateNodeUnique: %s unknown object type [%s]" % (self.getName(), PrototypeTypeName))
            return None

        node = PrototypeType.generatePrototypeNode(**PrototypeParams)

        return node

    def tryGenerateObjectUnique(self, objectName, prototypeName, EntityHierarchy=True, **prototypeParams):
        if self.hasPrototype(prototypeName) is False:
            return None

        return self.generateObjectUnique(objectName, prototypeName, EntityHierarchy=EntityHierarchy, **prototypeParams)

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
        if _DEVELOPMENT is True:
            if obj.isUnique() is False and self.hasObject(name) is True:
                Trace.log("Object", 0, "ChildObject._addObject '%s' already exist child '%s' [%d]" % (self.name, name, id(obj)))

                return False

        obj.removeFromParent()

        obj.setParent(self)
        obj.setGroup(self)

        obj.setUnique(False)

        self.child.append(name, obj)

        return True

    def _addObjectUnique(self, obj):
        obj.setParent(self)
        obj.setGroup(self)

        self.child_unique.append(obj)

    def removeObject(self, obj):
        name = obj.getName()

        if _DEVELOPMENT is True:
            if isinstance(obj, str) is True:
                Trace.log("Object", 0, "ChildObject.removeObject '%s' invalid remove by name '%s'" % (self.name, obj))
                return

            if obj.isUnique() is False and self.hasObject(name) is False:
                Trace.log("Object", 0, "ChildObject.removeObject '%s' invalid remove child '%s' [%d] don't found" % (self.name, name, id(obj)))
                return

        obj.setParent(None)

        if obj.isUnique() is False:
            self.child.remove(name)
        else:
            self.child_unique.remove(obj)
            pass

    def getObject(self, name):
        obj = self.child.get(name)

        if obj is None:
            Trace.log("Object", 0, "ChildObject '%s:%s' not found child '%s'" % (self.getGroupName(), self.name, name))

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

        self.visitChildren(cb)
        pass

    def visitChildren(self, cb):
        for child in self.child:
            child.visitObjects(cb)
            pass

        for child in self.child_unique:
            child.visitObjects(cb)
            pass
        pass

    def visitObjectsBreakOnFalse(self, cb):
        if cb(self) is False:
            return False

        return self.visitChildrenBreakOnFalse(cb)

    def visitChildrenBreakOnFalse(self, cb):
        for child in self.child:
            if child.visitObjectsBreakOnFalse(cb) is False:
                return False

        for child in self.child_unique:
            if child.visitObjectsBreakOnFalse(cb) is False:
                return False

        return True

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

        for obj in objects:
            obj.setParent(None)
            obj._onDestroySelf()

        self.child = None

        if _DEVELOPMENT is True:
            for obj in self.child_unique:
                if obj.isDestroy() is True:
                    continue
                Trace.log("Object", 0, "ChildObject._onDestroy: Unique child '%s' not destroyed '%s'" % (self.name, obj.getName()))
                pass
            pass

        self.child_unique = None

        self.prototypes = None