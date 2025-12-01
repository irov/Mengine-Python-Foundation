from Foundation.Actor import Actor
from Foundation.Initializer import Initializer

class BaseEntity(Actor, Initializer):
    __metaclass__ = baseslots("object", "node")

    @staticmethod
    def declareORM(Type):
        Actor.declareORM(Type)

        Type.addAction("Enable", Update=BaseEntity._updateEnable)
        Type.addAction("Interactive", Update=BaseEntity._updateRefcountInteractive)
        Type.addAction("BlockInteractive", Update=BaseEntity._updateBlockInteractive)

        Type.addAction("Position", Initialize=False, Update=BaseEntity.__updatePosition)
        Type.addAction("Scale", Initialize=False, Update=BaseEntity.__updateScale)
        Type.addAction("Origin", Initialize=False, Update=BaseEntity.__updateOrigin)
        Type.addAction("Orientation", Initialize=False, Update=BaseEntity.__updateOrientation)
        Type.addAction("Alpha", Initialize=False, Update=BaseEntity.__updateAlpha)
        Type.addAction("RGB", Initialize=False, Update=BaseEntity.__updateRGB)
        pass

    def __init__(self):
        super(BaseEntity, self).__init__()

        self.object = None
        self.node = None
        pass

    def setName(self, name):
        self.node.setName(name)
        pass

    def getName(self):
        return self.node.getName()

    def getObjectType(self):
        if self.object is None:
            return None

        return self.object.getType()

    def getObjectName(self):
        if self.object is None:
            return None

        return self.object.getName()

    def addChild(self, node):
        self.node.addChild(node)
        pass

    def removeChild(self, node):
        self.node.removeChild(node)
        pass

    def createChild(self, type):
        return self.node.createChild(type)

    def removeFromParent(self):
        self.node.removeFromParent()
        pass

    def removeChildren(self):
        self.node.removeChildren()
        pass

    def addChildFront(self, node):
        self.node.addChildFront(node)
        pass

    def enable(self):
        self.node.enable()
        pass

    def disable(self):
        self.node.disable()
        pass

    def isActivate(self):
        return self.node.isActivate()

    def getLocalPosition(self):
        return self.node.getLocalPosition()

    def getWorldPosition(self):
        return self.node.getWorldPosition()

    def getScreenPosition(self):
        return self.node.getScreenPosition()

    def getCameraPosition(self, Camera):
        return Mengine.getCameraPosition(Camera, self.node)

    def _actorFailed(self, typeActor, msg):
        Trace.log("BaseEntity", 0, "Entity %s Type %s failed: %s" % (self.getName(), typeActor.__name__, msg))
        pass

    def onCreate(self, node):
        self.node = node
        pass

    def onDestroy(self):
        if _DEVELOPMENT is True:
            if self.object is not None:
                if self.object.hasEntity() is True:
                    Trace.log("Entity", 0, "BaseEntity.onDestroy %s:%s have object!" % (self.getObjectType(), self.getObjectName()))
                    pass
                pass
            pass

        self._onDestroy()

        self.node = None
        pass

    def _onDestroy(self):
        pass

    def _onInitialize(self, obj):
        super(BaseEntity, self)._onInitialize(obj)

        if _DEVELOPMENT is True:
            params = obj.getParams()
            consts = obj.getConsts()

            if self.validateAction(params, consts) is False:
                self.initializeFailed("Entity '%s:%s' invalid initialized: incorrect actions for params" % (obj.getType(), obj.getName()))
                pass
            pass

        self.object = obj
        pass

    def _onFinalize(self):
        super(BaseEntity, self)._onFinalize()

        if _DEVELOPMENT is True:
            if Mengine.is_class(self.node) is False:
                Trace.log("BaseEntity", 0, "Entity %s:%s _onFinalize self is not class" % (self.getObjectType(), self.getObjectName()))
                return

            if Mengine.is_wrap(self.node) is False:
                Trace.log("BaseEntity", 0, "Entity %s:%s _onFinalize self is unwrap" % (self.getObjectType(), self.getObjectName()))
                return

            if self.object.isActive() is True:
                Trace.log("BaseEntity", 0, "Entity '%s:%s' has been destroyed while the object was still alive. Probably you've forgot to unlink it from another Entity (%s)" % (self.getObjectType(), self.getObjectName(), self.object.getParent()))
                return
            pass

        self.node.disable()
        pass

    def onRemoveObject(self):
        self.object = None
        pass

    def onRemoveNode(self):
        Mengine.destroyEntity(self.node)
        self.node = None
        pass

    def _onInitializeFailed(self, msg):
        Trace.log("BaseEntity", 0, "Entity '%s:%s' initialize failed '%s'" % (self.getObjectType(), self.getName(), msg))
        pass

    def _onFinalizeFailed(self, msg):
        Trace.log("BaseEntity", 0, "Entity '%s:%s' finalize failed '%s'" % (self.getObjectType(), self.getName(), msg))
        pass

    def onRestore(self):
        self._onRestore()

        consts = self.object.getConsts()
        self.updateActions(consts, False, True)

        params = self.object.getParams()
        self.updateActions(params, False, True)

        self._onRestored()
        pass

    def _onRestore(self):
        pass

    def _onRestored(self):
        pass

    def onCompile(self):
        self._onCompile()
        pass

    def _onCompile(self):
        pass

    def onPreparation(self):
        self._onPreparation()
        pass

    def _onPreparation(self):
        pass

    def _isActorActive(self):
        return self.node.isActivate()

    def onActivate(self):
        if self.object is None:
            Trace.log("BaseEntity", 0, "Entity.onActivate %s object is None" % (self.getName()))
            pass

        self._onActivate()

        consts = self.object.getConsts()
        self.updateActions(consts, True, False)

        params = self.object.getParams()
        self.updateActions(params, True, False)
        pass

    def _onActivate(self):
        pass

    def onPreparationDeactivate(self):
        self._onPreparationDeactivate()
        pass

    def _onPreparationDeactivate(self):
        pass

    def onDeactivate(self):
        if self.isInitialized() is False:
            return
            pass

        self._onDeactivate()
        pass

    def _onDeactivate(self):
        pass

    def onRun(self):
        if self.object is None:
            Trace.log("BaseEntity", 0, "Entity.onRun %s object is None" % (self.getName()))
            pass

        if self._onRun() is False:
            Trace.log("BaseObject", 0, "Entity.onRun '%s' failed" % (self.getName()))
            return False

        return True

    def _onRun(self):
        return True

    def getObject(self):
        return self.object

    def getSubEntity(self, name):
        obj = self.object.getObject(name)

        if obj is None:
            Trace.log("BaseEntity", 0, "Entity '%s:%s' getSubEntity: not exist %s" % (self.getObjectType(), self.getName(), name))
            pass

        entity = obj.getEntity()

        return entity

    def _updateEnable(self, value):
        if value is True:
            self.node.enable()
            pass
        else:
            self.node.disable()
            self.node.release()
            pass

        self._onUpdateEnable(value)
        pass

    def _onUpdateEnable(self, value):
        pass

    def _updateRefcountInteractive(self, value):
        interactive = self.object.isInteractive()

        self._updateInteractive(interactive)
        pass

    def _updateInteractive(self, value):
        pass

    def _updateBlockInteractive(self, value):
        pass

    def __updatePosition(self, value):
        self.node.setLocalPosition(value)
        pass

    def __updateScale(self, value):
        self.node.setScale(value)
        pass

    def __updateOrigin(self, value):
        self.node.setOrigin(value)
        pass

    def __updateOrientation(self, orientation):
        self.node.setOrientation(orientation)
        pass

    def __updateAlpha(self, alpha):
        render = self.node.getRender()
        if render is not None:
            render.setLocalAlpha(alpha)
            pass
        pass

    def __updateRGB(self, rgb):
        render = self.node.getRender()
        render.setLocalColorRGB(rgb[0], rgb[1], rgb[2])
        pass
    pass