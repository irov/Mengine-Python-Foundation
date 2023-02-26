from Foundation.Actor import Actor
from Foundation.Initializer import Initializer

class BaseEntity(Actor, Initializer):
    __metaclass__ = baseslots("object", "node")

    @staticmethod
    def declareORM(Type):
        Actor.declareORM(Type)

        Type.addAction(Type, "Enable", Update=BaseEntity._updateEnable)
        Type.addAction(Type, "Interactive", Update=BaseEntity._updateRefcountInteractive)
        Type.addAction(Type, "BlockInteractive", Update=BaseEntity._updateBlockInteractive)

        Type.addAction(Type, "Position", Initialize=False, Update=BaseEntity.__updatePosition)
        Type.addAction(Type, "Scale", Initialize=False, Update=BaseEntity.__updateScale)
        Type.addAction(Type, "Origin", Initialize=False, Update=BaseEntity.__updateOrigin)
        Type.addAction(Type, "Orientation", Initialize=False, Update=BaseEntity.__updateOrientation)
        Type.addAction(Type, "Alpha", Initialize=False, Update=BaseEntity.__updateAlpha)
        Type.addAction(Type, "RGB", Initialize=False, Update=BaseEntity.__updateRGB)
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
        pass

    def addChild(self, node):
        self.node.addChild(node)
        pass

    def removeChild(self, node):
        self.node.removeChild(node)
        pass

    def createChild(self, type):
        return self.node.createChild(type)
        pass

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
        pass

    def getLocalPosition(self):
        return self.node.getLocalPosition()
        pass

    def getWorldPosition(self):
        return self.node.getWorldPosition()
        pass

    def getCameraPosition(self, Camera):
        return Menge.getCameraPosition(Camera, self.node)
        pass

    @staticmethod
    def _actorFailed(typeActor, msg):
        Trace.log("BaseEntity", 0, "EntityType %s failed: %s" % (typeActor.__name__, msg))
        pass

    def onCreate(self, node):
        self.node = node
        pass

    def onDestroy(self):
        if _DEVELOPMENT is True:
            if self.object is not None:
                if self.object.hasEntity() is True:
                    Trace.log("Entity", 0, "BaseEntity.onDestroy %s:%s have object!" % (self.object.getType(), self.object.getName()))
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

        self.object = obj

        if _DEVELOPMENT is True:
            consts = obj.getConsts()
            if self.validateAction(consts) is False:
                self.initializeFailed("Entity '%s:%s' invalid initialized: incorrect actions for consts" % (self.object.getType(), self.object.getName()))
                pass

            params = obj.getParams()
            if self.validateAction(params) is False:
                self.initializeFailed("Entity '%s:%s' invalid initialized: incorrect actions for params" % (self.object.getType(), self.object.getName()))
                pass
            pass
        pass

    def _onFinalize(self):
        super(BaseEntity, self)._onFinalize()

        if _DEVELOPMENT is True:
            if Menge.is_class(self.node) is False:
                Trace.log("BaseEntity", 0, "Entity %s:%s _onFinalize self is not class" % (self.object.getType(), self.object.getName()))
                return
                pass

            if Menge.is_wrap(self.node) is False:
                Trace.log("BaseEntity", 0, "Entity %s:%s _onFinalize self is unwrap" % (self.object.getType(), self.object.getName()))
                return
                pass

            if self.object.isActive() is True:
                Trace.log("BaseEntity", 0, "Entity '%s:%s' has been destroyed while the object was still alive. Probably you've forgot to unlink it from another Entity (%s)" % (self.object.getName(), self.object.getType(), self.object.getParent()))
                return
                pass
            pass

        self.node.disable()
        pass

    def onRemoveObject(self):
        self.object = None
        pass

    def onRemoveNode(self):
        Menge.destroyEntity(self.node)
        self.node = None
        pass

    def _onInitializeFailed(self, msg):
        Trace.log("BaseEntity", 0, "Entity '%s:%s' initialize failed '%s'" % (self.object.getType(), self.getName(), msg))
        pass

    def _onFinalizeFailed(self, msg):
        Trace.log("BaseEntity", 0, "Entity '%s:%s' finalize failed '%s'" % (self.object.getType(), self.getName(), msg))
        pass

    def onRestore(self):
        self._onRestore()

        consts = self.object.getConsts()
        self.callActions(consts, False, True, "Update")

        params = self.object.getParams()
        self.callActions(params, False, True, "Update")

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
        pass

    def onActivate(self):
        if self.object is None:
            Trace.log("BaseEntity", 0, "Entity.onActivate %s object is None" % (self.getName()))
            pass

        self._onActivate()

        consts = self.object.getConsts()
        self.callActions(consts, True, False, "Update")

        params = self.object.getParams()
        self.callActions(params, True, False, "Update")
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
            pass

        return True
        pass

    def _onRun(self):
        return True
        pass

    def getObject(self):
        return self.object
        pass

    def getSubEntity(self, name):
        obj = self.object.getObject(name)

        if obj is None:
            Trace.log("BaseEntity", 0, "Entity '%s:%s' getSubEntity: not exist %s" % (self.object.getType(), self.getName(), name))
            pass

        entity = obj.getEntity()

        return entity
        pass

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