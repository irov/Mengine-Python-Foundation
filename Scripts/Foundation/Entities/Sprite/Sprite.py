from Foundation.Entity.BaseEntity import BaseEntity

class Sprite(BaseEntity):
    @staticmethod
    def declareORM(Type):
        BaseEntity.declareORM(Type)

        Type.addAction("SpriteResourceName", Update=Sprite.__updateSpriteResourceName)
        Type.addAction("ExtraResource", Update=Sprite.__updateExtraResource)
        pass

    def __updateSpriteResourceName(self, value):
        if value is None:
            return

        surface = self.shape.getSurface()
        surface.setResourceImage(value)
        pass

    def __updateExtraResource(self, value):
        if value is None:
            return

        resource = Mengine.getResourceReference(value)

        surface = self.shape.getSurface()
        surface.setResourceImage(resource)
        pass

    def __init__(self):
        super(Sprite, self).__init__()

        self.shape = None
        pass

    def _onInitialize(self, obj):
        super(Sprite, self)._onInitialize(obj)

        shape = self.createChild("ShapeQuadFixed")

        name = self.getName()
        shape.setName(name)

        surface = Mengine.createSurface("SurfaceImage")
        surface.setName(name)

        shape.setSurface(surface)
        shape.enable()

        self.shape = shape
        pass

    def _onFinalize(self):
        super(Sprite, self)._onFinalize()

        Mengine.destroyNode(self.shape)
        self.shape = None
        pass

    def getSize(self):
        return self.shape.getSurfaceSize()

    def getSprite(self):
        return self.shape
    pass