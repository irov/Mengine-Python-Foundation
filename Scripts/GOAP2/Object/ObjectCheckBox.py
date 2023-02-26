from DemonObject import DemonObject

class ObjectCheckBox(DemonObject):
    @staticmethod
    def declareORM(Type):
        DemonObject.declareORM(Type)

        Type.addParam(Type, "Polygon")
        Type.addParam(Type, "State")
        Type.addParam(Type, "BlockState")
        Type.addParam(Type, "KeyTag")
        pass

    def _onParams(self, params):
        super(ObjectCheckBox, self)._onParams(params)

        self.initParam("Polygon", params, [])
        self.initParam("State", params, False)
        self.initParam("BlockState", params, False)
        self.initParam("KeyTag", params, None)
        pass
    pass