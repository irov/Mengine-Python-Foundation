from Object import Object

class ObjectSprite(Object):
    @staticmethod
    def declareORM(Type):
        Object.declareORM(Type)

        Type.declareResource("SpriteResourceName")
        Type.declareParam("ExtraResource")

    def _onParams(self, params):
        super(ObjectSprite, self)._onParams(params)

        self.initResource("SpriteResourceName", params)
        self.initParam("ExtraResource", params, None)

    @classmethod
    def generatePrototypeNode(cls, **PrototypeParams):
        Name = PrototypeParams.get("Name", "")
        SpriteResourceName = PrototypeParams.get("SpriteResourceName")
        ExtraResource = PrototypeParams.get("ExtraResource")

        shape = Mengine.createNode("ShapeQuadFixed")
        shape.setName(Name)

        surface = Mengine.createSurface("SurfaceImage")
        surface.setName(Name)

        if ExtraResource is not None:
            resource = Mengine.getResourceReference(ExtraResource)
            surface.setResourceImage(resource)
        else:
            resource = Mengine.getResourceReference(SpriteResourceName)
            surface.setResourceImage(resource)
            pass

        shape.setSurface(surface)
        shape.enable()

        return shape
