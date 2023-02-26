from Foundation.Object.BaseObject import BaseObject

from Foundation.Params import DefaultParam

class EntityObject(BaseObject):
    PARAMS_Enable = True
    PARAMS_Interactive = 0
    PARAMS_Position = DefaultParam((0.0, 0.0, 0.0))
    PARAMS_Scale = DefaultParam((1.0, 1.0, 1.0))
    PARAMS_Origin = DefaultParam((0.0, 0.0, 0.0))
    PARAMS_Orientation = DefaultParam((0.0, 0.0, 0.0))
    PARAMS_Alpha = DefaultParam(1.0)
    PARAMS_RGB = DefaultParam((1.0, 1.0, 1.0))

    def __init__(self):
        super(EntityObject, self).__init__()

        self.__dynamicInteractive = 0
        self.entityType = None
        pass

    def setEntityType(self, entityType):
        self.entityType = entityType
        pass

    def getEntityType(self):
        return self.entityType
        pass

    @staticmethod
    def declareORM(Type):
        BaseObject.declareORM(Type)

        Type.addParam(Type, "Enable")
        Type.addParam(Type, "BlockInteractive")
        Type.addParam(Type, "Position")
        Type.addParam(Type, "Scale")
        Type.addParam(Type, "Origin")
        Type.addParam(Type, "Orientation")
        Type.addParam(Type, "Alpha")
        Type.addParam(Type, "RGB")
        pass

    def _onParams(self, params):
        super(EntityObject, self)._onParams(params)

        self.initParam("Enable", params, self.PARAMS_Enable)
        self.initParam("Interactive", params, self.PARAMS_Interactive)
        self.initParam("BlockInteractive", params, False)
        self.initParam("Position", params, self.PARAMS_Position)
        self.initParam("Scale", params, self.PARAMS_Scale)
        self.initParam("Origin", params, self.PARAMS_Origin)
        self.initParam("Orientation", params, self.PARAMS_Orientation)
        self.initParam("Alpha", params, self.PARAMS_Alpha)
        self.initParam("RGB", params, self.PARAMS_RGB)
        pass

    def _onLoadParams(self):
        if self.isActive() is True:
            self.onEntityRestore()
            pass
        pass

    def _getActor(self):
        if self.isActive() is False:
            return None
            pass

        entity = self.getEntity()
        return entity
        pass

    def setParamInteractive(self, value):
        if isinstance(value, bool) is False:
            Trace.log("Entity", 0, "Entity.setParamInteractive %s:%s invalid value %s need bool [True|False] is refcounting!" % (self.getGroupName(), self.getName()))
            return
            pass

        Interactive = self.getParam("Interactive")

        if value is True:
            Interactive += 1
        else:
            Interactive -= 1
            pass

        self.setParam("Interactive", Interactive)

        if _DEVELOPMENT is True:
            Interactive = self.getParam("Interactive")
            refcount = Interactive + self.__dynamicInteractive

            if refcount == -1:
                Trace.log("Entity", 0, "Entity.setParamInteractive %s:%s negative interactive refcount!" % (self.getGroupName(), self.getName()))
                # return
                pass
            pass
        pass

    def setInteractive(self, value):
        if isinstance(value, bool) is False:
            Trace.log("Entity", 0, "Entity.setDynamicInteractive %s:%s invalid value %s need bool [True|False] is refcounting!" % (self.getGroupName(), self.getName(), value))
            return
            pass

        if value is True:
            self.__dynamicInteractive += 1
            pass
        else:
            self.__dynamicInteractive -= 1
            pass

        Interactive = self.getParam("Interactive")
        self.setParam("Interactive", Interactive)

        if _DEVELOPMENT is True:
            refcount = Interactive + self.__dynamicInteractive

            if refcount == -1:
                Trace.log("Entity", 0, "Entity.setDynamicInteractive %s:%s negative interactive refcount!" % (self.getGroupName(), self.getName()))
                # return
                pass
            pass
        pass

    def getInteractive(self):
        Interactive = self.getParam("Interactive")

        refcount = Interactive + self.__dynamicInteractive

        return refcount
        pass

    def isInteractive(self):
        Interactive = self.getParam("Interactive")

        refcount = Interactive + self.__dynamicInteractive

        return refcount > 0
        pass

    def getInteractiveRefcount(self):
        Interactive = self.getParam("Interactive")

        refcount = Interactive + self.__dynamicInteractive

        return refcount
        pass

    def onGenerate(self):
        entity = self._onGenerate()

        return entity
        pass

    def _onGenerate(self):
        entity = Mengine.createEntity(self.entityType)

        name = self.getName()
        entity.node.setName(name)

        entity.node.disable()

        return entity
        pass

    def _onInitialize(self):
        super(EntityObject, self)._onInitialize()
        pass

    def _onFinalize(self):
        super(EntityObject, self)._onFinalize()
        pass

    def initializeEntity(self):
        entity = self.onGenerate()

        if entity is None:
            Trace.log("Object", 0, "Object.initializeEntity: %s:%s not generate" % (self.getGroup().getName(), self.name))

            return None
            pass

        if entity.onInitialize(self) is False:
            Trace.log("Object", 0, "Object.initializeEntity: %s:%s not initialize" % (self.getGroup().getName(), self.name))

            return None
            pass

        self.setEntity(entity)

        return entity
        pass

    def restoreTransformation(self):
        self.updateParam()
        pass

    def _onActivate(self):
        entity = self.initializeEntity()

        if entity is None:
            Trace.log("Object", 0, "EntityObject %s invalid activate" % (self.getName()))

            return False
            pass

        return True
        pass

    def _onDeactivate(self):
        super(EntityObject, self)._onDeactivate()

        if _DEVELOPMENT is True:
            self.__onDeactivateTestObject()
            pass

        entity = self.entity
        self.setEntity(None)

        entity.disable()

        entity.onFinalize()
        entity.onRemoveObject()
        entity.onRemoveNode()
        pass

    def __onDeactivateTestObject(self):
        if Mengine.is_class(self.entity.node) is False:
            Trace.log("Object", 0, "EntityObject._onDeactivate %s but entity is not class!!" % (self.getName()))
            return
            pass

        if Mengine.is_wrap(self.entity.node) is False:
            Trace.log("Object", 0, "EntityObject._onDeactivate %s but entity is unwrap!!" % (self.getName()))
            return False
            pass

        EntityParent = self.entity.node.getParent()

        if EntityParent is None:
            pass
        elif Mengine.isHomeless(self.entity.node) is True:
            ObjectParent = self.getParent()

            if ObjectParent is not None:
                # Trace.log("Object", 0, "Object '%s:%s' entity is homeless but object has parent %s:%s"%(self.getName(), self.getGroupName(), ObjectParent.getName(), ObjectParent.getGroupName()))
                return False
                pass
            pass
        else:
            ObjectParent = self.getParent()

            if ObjectParent is None:
                Trace.log("Object", 0, "Object '%s:%s' not parent" % (self.getName(), self.getGroupName()))
                return False
                pass

            from Foundation.Group import Group

            if issubclass(type(ObjectParent), Group) is True:
                LayerName = self.getLayerName()
                ObjectParentEntity = ObjectParent.getLayer(LayerName)
            else:
                if ObjectParent.isActive() is False:
                    return True
                    pass

                ObjectParentEntity = ObjectParent.getEntity()
                pass

            if EntityParent is not ObjectParentEntity:
                Trace.log("Object", 0, "EntityObject '%s:%s' entity remove, but entity link not parent '%s' != '%s'" % (self.getName(), self.getGroupName(), EntityParent.getName(), ObjectParent.getName()))
                pass
            pass

        return True
        pass

    def _onRun(self):
        if self.entity is None:
            return False
            pass

        self.entity.onRun()

        return True
        pass

    def translate(self, delta):
        Position = self.getPosition()

        Position[0] += delta[0]
        Position[1] += delta[1]

        self.setPosition(Position)
        pass
    pass