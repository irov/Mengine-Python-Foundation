from Foundation.Initializer import Initializer
from Foundation.Params import Params

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

    def setName(self, name):
        self.name = name
        pass

    def getName(self):
        return self.name

    def setGroup(self, group):
        self.Group = group
        pass

    def getGroup(self):
        return self.Group

    def setLayerName(self, layerName):
        self.layerName = layerName

    def getLayerName(self):
        return self.layerName

    def _onParams(self, params):
        super(BaseObject, self)._onParams(params)
        pass

    def getType(self):
        return type(self).__name__

    def setSaving(self, saving):
        self.saving = saving
        pass

    def isSaving(self):
        return self.saving

    def setEntity(self, entity):
        self.entity = entity
        pass

    def getEntity(self):
        if self.isActive() is False:
            Trace.log("Object", 0, "BaseObject.getEntity: '%s:%s' (type '%s') not active" % (self.getGroupName(), self.getName(), self.getType()))
            return None

        return self.entity

    def getEntityNode(self):
        if self.isActive() is False:
            Trace.log("Object", 0, "BaseObject.getEntityNode: '%s:%s' (type '%s') not active" % (self.getGroupName(), self.getName(), self.getType()))
            return None

        return self.entity.node

    def onEntityRestore(self):
        if self.isActive() is False:
            Trace.log("Object", 0, "BaseObject.onEntityRestore: '%s:%s' (type '%s') not active" % (self.getGroupName(), self.getName(), self.getType()))
            return

        self.entity.onRestore()

    def isEntityActivate(self):
        if self.hasEntity() is False:
            return False

        if self.entity.isActivate() is False:
            return False

        return True

    def hasEntity(self):
        return self.entity is not None

    def onLoader(self):
        self._onLoader()
        self.loaded = True

    def _onLoader(self):
        pass

    def getGroupName(self):
        Group = self.getGroup()

        if Group is None:
            return None

        GroupName = Group.getName()

        return GroupName

    def removeFromParent(self):
        # if self.isActive() is True:
        #     entity = self.getEntity()
        #     entity.removeFromParent()

        if self.isActive() is True:
            entity = self.getEntity()
            if entity is not None:
                entity.removeFromParent()
            else:
                Trace.log("Object", 0, "BaseObject.removeFromParent '%s:%s' (type '%s') has no entity" % (self.getGroupName(), self.getName(), self.getType()))

        if self.parent is None:
            return

        name = self.getName()
        self.parent.removeObject(name)
        self.parent = None

    def returnToParent(self):
        if self.parent is None:
            return

        if self.parent.entity is None:
            return

        if self.entity is None:
            return

        parentEntity = self.parent.entity

        parentEntity.addChild(self.entity.node)

    def setParent(self, parent):
        self.parent = parent

    def getParent(self):
        return self.parent

    def isActive(self):
        return self.active > 0

    def isDestroy(self):
        return self.__destroy

    def onDestroy(self):
        if self.__destroy is True:
            Trace.log("Object", 0, "BaseObject.onDestroy already destroyed '%s:%s' (type '%s')" % (self.getGroupName(), self.getName(), self.getType()))
            return

        self.removeFromParent()

        if self.isInitialized() is True:
            self.onFinalize()

        self._onDestroy()
        self.Group = None

        self.removeParams()

        self.__destroy = True

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

        self.active += 1

        if self.active > 1:
            return True

        if self._onActivate() is False:
            Trace.log("BaseObject", 0, "BaseObject.onActivate '%s:%s' (type '%s') _onActivate failed" % (self.getGroupName(), self.getName(), self.getType()))
            return False

        return True

    def _onActivate(self):
        return True

    def onDeactivate(self):
        if self.active == 0:
            Trace.log("BaseObject", 0, "BaseObject '%s:%s' (type '%s') already deactivated" % (self.getGroupName(), self.getName(), self.getType()))
            return

        self.active -= 1

        if self.active > 0:
            return

        self._onDeactivate()

    def _onDeactivate(self):
        pass

    def onRun(self):
        if self.isInitialized() is False:
            Trace.log("BaseObject", 0, "BaseObject.onRun '%s:%s' (type '%s') activate is failed - not initialize" % (self.getGroupName(), self.getName(), self.getType()))
            return False

        if self._onRun() is False:
            Trace.log("BaseObject", 0, "BaseObject.onRun '%s:%s' (type '%s') failed" % (self.getGroupName(), self.getName(), self.getType()))
            return False

        return True

    def _onRun(self):
        return True

    def _checkParamExtraValue(self, value):
        type_value = type(value)

        if issubclass(type_value, BaseObject) is True:
            return True

        return False

    def visitObjects(self, cb):
        cb(self)
        pass

    def visitChildren(self, cb):
        pass

    def visitObjectsBreakOnFalse(self, cb):
        if cb(self) is False:
            return False

        return True

    def visitChildrenBreakOnFalse(self, cb):
        pass

    def visitParentBrakeOnFalse(self, cb):
        parent = self.getParent()

        if parent is None:
            return False

        parent.visitParentBrakeOnFalse(cb)

        if cb(parent) is False:
            return False

        return True
