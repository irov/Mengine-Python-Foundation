from DemonObject import DemonObject

class ObjectCheckBox(DemonObject):
    @staticmethod
    def declareORM(Type):
        DemonObject.declareORM(Type)

        Type.declareParam("Polygon")
        Type.declareParam("State")
        Type.declareParam("BlockState")
        Type.declareParam("KeyTag")
        pass

    def _onParams(self, params):
        super(ObjectCheckBox, self)._onParams(params)

        self.initParam("Polygon", params, [])
        self.initParam("State", params, False)
        self.initParam("BlockState", params, False)
        self.initParam("KeyTag", params, None)
        pass
    pass