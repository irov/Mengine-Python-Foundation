from Object import Object

class ObjectSprite(Object):
    @staticmethod
    def declareORM(Type):
        Object.declareORM(Type)

        Type.addResource(Type, "SpriteResourceName")
        Type.addParam(Type, "ExtraResource")

    def _onParams(self, params):
        super(ObjectSprite, self)._onParams(params)

        self.initResource("SpriteResourceName", params)
        self.initParam("ExtraResource", params, None)