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

    def setEntityType(self, entityType):
        self.entityType = entityType

    def getEntityType(self):
        return self.entityType

    @staticmethod
    def declareORM(Type):
        BaseObject.declareORM(Type)

        Type.declareParam("Enable")
        Type.declareParam("BlockInteractive")
        Type.declareParam("Position")
        Type.declareParam("Scale")
        Type.declareParam("Origin")
        Type.declareParam("Orientation")
        Type.declareParam("Alpha")
        Type.declareParam("RGB")

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

    def _onLoadParams(self):
        if self.isActive() is True:
            self.onEntityRestore()

    def _getActor(self):
        if self.isActive() is False:
            return None

        entity = self.getEntity()
        return entity

    def setParamInteractive(self, value):
        if isinstance(value, bool) is False:
            Trace.log("Entity", 0, "Entity.setParamInteractive %s:%s invalid value %s need bool [True|False] is refcounting!" % (self.getGroupName(), self.getName(), value))
            return

        Interactive = self.getParam("Interactive")

        if value is True:
            Interactive += 1
        else:
            Interactive -= 1

        self.setParam("Interactive", Interactive)

        if _DEVELOPMENT is True:
            Interactive = self.getParam("Interactive")
            refcount = Interactive + self.__dynamicInteractive

            if refcount == -1:
                Trace.log("Entity", 0, "Entity.setParamInteractive %s:%s negative interactive refcount!" % (self.getGroupName(), self.getName()))
                # return

    def setInteractive(self, value):
        if isinstance(value, bool) is False:
            Trace.log("Entity", 0, "Entity.setDynamicInteractive %s:%s invalid value %s need bool [True|False] is refcounting!" % (self.getGroupName(), self.getName(), value))
            return

        if value is True:
            self.__dynamicInteractive += 1
        else:
            self.__dynamicInteractive -= 1

        Interactive = self.getParam("Interactive")
        self.setParam("Interactive", Interactive)

        if _DEVELOPMENT is True:
            refcount = Interactive + self.__dynamicInteractive

            if refcount == -1:
                Trace.log("Entity", 0, "Entity.setDynamicInteractive %s:%s negative interactive refcount!" % (self.getGroupName(), self.getName()))
                # return

    def getInteractive(self):
        Interactive = self.getParam("Interactive")

        refcount = Interactive + self.__dynamicInteractive

        return refcount

    def isInteractive(self):
        Interactive = self.getParam("Interactive")

        refcount = Interactive + self.__dynamicInteractive

        return refcount > 0

    def getInteractiveRefcount(self):
        Interactive = self.getParam("Interactive")

        refcount = Interactive + self.__dynamicInteractive

        return refcount

    def onGenerate(self):
        entity = self._onGenerate()

        return entity

    def _onGenerate(self):
        entity = Mengine.createEntity(self.entityType)

        name = self.getName()
        entity.node.setName(name)

        entity.node.disable()

        return entity

    def _onInitialize(self):
        super(EntityObject, self)._onInitialize()

    def _onFinalize(self):
        super(EntityObject, self)._onFinalize()

    def initializeEntity(self):
        entity = self.onGenerate()

        if entity is None:
            Trace.log("Object", 0, "Object.initializeEntity: %s:%s not generate" % (self.getGroup().getName(), self.name))

            return None

        if entity.onInitialize(self) is False:
            Trace.log("Object", 0, "Object.initializeEntity: %s:%s not initialize" % (self.getGroup().getName(), self.name))

            return None

        self.setEntity(entity)

        return entity

    def restoreTransformation(self):    # fixme: unused?
        self.updateParam()

    def _onActivate(self):
        entity = self.initializeEntity()

        if entity is None:
            Trace.log("Object", 0, "EntityObject %s invalid activate" % (self.getName()))

            return False

        return True

    def _onDeactivate(self):
        super(EntityObject, self)._onDeactivate()

        if _DEVELOPMENT is True:
            self.__onDeactivateTestObject()

        entity = self.entity
        self.setEntity(None)

        entity.disable()

        entity.onFinalize()
        entity.onRemoveObject()
        entity.onRemoveNode()

    def __onDeactivateTestObject(self):
        if Mengine.is_class(self.entity.node) is False:
            Trace.log("Object", 0, "EntityObject._onDeactivate %s but entity is not class!!" % (self.getName()))
            return

        if Mengine.is_wrap(self.entity.node) is False:
            Trace.log("Object", 0, "EntityObject._onDeactivate %s but entity is unwrap!!" % (self.getName()))
            return False

        EntityParent = self.entity.node.getParent()

        if EntityParent is None:
            pass
        elif Mengine.isHomeless(self.entity.node) is True:
            ObjectParent = self.getParent()

            if ObjectParent is not None:
                # Trace.log("Object", 0, "Object '%s:%s' entity is homeless but object has parent %s:%s"%(self.getName(), self.getGroupName(), ObjectParent.getName(), ObjectParent.getGroupName()))
                return False
        else:
            ObjectParent = self.getParent()

            if ObjectParent is None:
                Trace.log("Object", 0, "Object '%s:%s' not parent" % (self.getName(), self.getGroupName()))
                return False

            from Foundation.Group import Group

            if issubclass(type(ObjectParent), Group) is True:
                LayerName = self.getLayerName()
                ObjectParentEntity = ObjectParent.getLayer(LayerName)
            else:
                if ObjectParent.isActive() is False:
                    return True

                ObjectParentEntity = ObjectParent.getEntity()

            if EntityParent is not ObjectParentEntity:
                Trace.log("Object", 0, "EntityObject '%s:%s' entity remove, but entity link not parent '%s' != '%s'" % (self.getName(), self.getGroupName(), EntityParent.getName(), ObjectParent.getName()))

        return True

    def _onRun(self):
        if self.entity is None:
            return False

        self.entity.onRun()

        return True

    def translate(self, delta):
        Position = self.getPosition()

        Position[0] += delta[0]
        Position[1] += delta[1]

        self.setPosition(Position)
