from GOAP2.Initializer import Initializer
from GOAP2.Params import Params

class BaseObject(Params, Initializer):
    def __init__(self):
        super(BaseObject, self).__init__()

        self.name = None

        self.parent = None
        self.Group = None

        self.active = 0
        self.__destroy = False

        self.entity = None

        self.saving = True
        self.loaded = False

        self.layerName = None
        self.prototypeName = None
        pass

    def setName(self, name):
        self.name = name
        pass

    def getName(self):
        return self.name
        pass

    def setGroup(self, group):
        self.Group = group
        pass

    def getGroup(self):
        return self.Group
        pass

    def setLayerName(self, layerName):
        self.layerName = layerName
        pass

    def getLayerName(self):
        return self.layerName
        pass

    def setPrototypeName(self, prototypeName):
        self.prototypeName = prototypeName
        pass

    def getPrototypeName(self):
        return self.prototypeName
        pass

    def _onParams(self, params):
        super(BaseObject, self)._onParams(params)
        pass

    def getType(self):
        return type(self).__name__
        pass

    def setSaving(self, saving):
        self.saving = saving
        pass

    def isSaving(self):
        return self.saving
        pass

    def setEntity(self, entity):
        self.entity = entity
        pass

    def getEntity(self):
        if self.isActive() is False:
            Trace.log("Object", 0, "BaseObject.getEntity: '%s:%s' (type '%s') not active" % (self.getGroupName(), self.getName(), self.getType()))
            return None
            pass

        return self.entity
        pass

    def getEntityNode(self):
        if self.isActive() is False:
            Trace.log("Object", 0, "BaseObject.getEntityNode: '%s:%s' (type '%s') not active" % (self.getGroupName(), self.getName(), self.getType()))

            return None
            pass

        return self.entity.node
        pass

    def onEntityRestore(self):
        if self.isActive() is False:
            Trace.log("Object", 0, "BaseObject.onEntityRestore: '%s:%s' (type '%s') not active" % (self.getGroupName(), self.getName(), self.getType()))
            return
            pass

        self.entity.onRestore()
        pass

    def hasEntity(self):
        return self.entity is not None
        pass

    def onLoader(self):
        self._onLoader()

        self.loaded = True
        pass

    def _onLoader(self):
        pass

    def getGroupName(self):
        Group = self.getGroup()

        if Group is None:
            return None
            pass

        GroupName = Group.getName()

        return GroupName
        pass

    def removeFromParent(self):
        # if self.isActive() is True:
        #     entity = self.getEntity()
        #     entity.removeFromParent()
        #     pass

        if self.isActive() is True:
            entity = self.getEntity()
            if entity is not None:
                entity.removeFromParent()
            else:
                Trace.log("Object", 0, "BaseObject.removeFromParent '%s:%s' (type '%s') has no entity" % (self.getGroupName(), self.getName(), self.getType()))

        if self.parent is None:
            return
            pass

        name = self.getName()
        self.parent.removeObject(name)
        self.parent = None
        pass

    def returnToParent(self):
        if self.parent is None:
            return
            pass

        if self.parent.entity is None:
            return
            pass

        if self.entity is None:
            return
            pass

        parentEntity = self.parent.entity

        parentEntity.addChild(self.entity.node)
        pass

    def setParent(self, parent):
        self.parent = parent
        pass

    def getParent(self):
        return self.parent
        pass

    def isActive(self):
        return self.active > 0
        pass

    def isDestroy(self):
        return self.__destroy
        pass

    def onDestroy(self):
        if self.__destroy is True:
            Trace.log("Object", 0, "BaseObject.onDestroy already destroyed '%s:%s' (type '%s')" % (self.getGroupName(), self.getName(), self.getType()))
            return
            pass

        self.removeFromParent()

        if self.isInitialized() is True:
            self.onFinalize()
            pass

        self._onDestroy()
        self.Group = None

        self.removeParams()

        self.__destroy = True
        pass

    def _onDestroy(self):
        pass

    def _onInitializeFailed(self, msg):
        Trace.log("Object", 0, "BaseObject initialize '%s:%s' (type '%s') is failed - %s" % (self.getGroupName(), self.name, self.getType(), msg))
        pass

    def _onFinalizeFailed(self, msg):
        Trace.log("Object", 0, "BaseObject finalize '%s:%s' (type '%s') is failed - %s" % (self.getGroupName(), self.name, self.getType(), msg))
        pass

    def _onInitialize(self):
        super(BaseObject, self)._onInitialize()
        pass

    def _onFinalize(self):
        super(BaseObject, self)._onFinalize()

        if self.isActive() is True:
            self.onDeactivate()
            pass
        pass

    def onActivate(self):
        if self.isInitialized() is False:
            Trace.log("BaseObject", 0, "BaseObject.onActivate '%s:%s' (type '%s') activate is failed - not initialize" % (self.getGroupName(), self.getName(), self.getType()))
            return False
            pass

        self.active += 1

        if self.active > 1:
            return True
            pass

        if self._onActivate() is False:
            Trace.log("BaseObject", 0, "BaseObject.onActivate '%s:%s' (type '%s') _onActivate failed" % (self.getGroupName(), self.getName(), self.getType()))
            return False
            pass

        return True
        pass

    def _onActivate(self):
        return True
        pass

    def onDeactivate(self):
        if self.active == 0:
            Trace.log("BaseObject", 0, "BaseObject '%s:%s' (type '%s') already deactivated" % (self.getGroupName(), self.getName(), self.getType()))
            return
            pass

        self.active -= 1

        if self.active > 0:
            return
            pass

        self._onDeactivate()
        pass

    def _onDeactivate(self):
        pass

    def onRun(self):
        if self.isInitialized() is False:
            Trace.log("BaseObject", 0, "BaseObject.onRun '%s:%s' (type '%s') activate is failed - not initialize" % (self.getGroupName(), self.getName(), self.getType()))
            return False
            pass

        if self._onRun() is False:
            Trace.log("BaseObject", 0, "BaseObject.onRun '%s:%s' (type '%s') failed" % (self.getGroupName(), self.getName(), self.getType()))
            return False
            pass

        return True
        pass

    def _onRun(self):
        return True
        pass

    def _checkParamExtraValue(self, value):
        type_value = type(value)
        if issubclass(type_value, BaseObject) is True:
            return True
            pass

        return False
        pass

    def visitObjects(self, cb):
        cb(self)
        pass

    def visitObjects2(self, cb):
        if cb(self) is False:
            return False
            pass

        return True
        pass

    def visitParentBrakeOnFalse(self, cb):
        parent = self.getParent()
        if parent is None:
            return False

        parent.visitParentBrakeOnFalse(cb)
        if cb(parent) is False:
            return False

        return True
        pass
    pass