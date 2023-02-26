from DemonObject import DemonObject

class ObjectSlider(DemonObject):
    PARAMS_Interactive = 1

    @staticmethod
    def declareORM(Type):
        DemonObject.declareORM(Type)

        Type.addParam(Type, "Slide")
        Type.addParam(Type, "Polygon")
        Type.addParam(Type, "Current")
        pass

    def _onParams(self, params):
        super(ObjectSlider, self)._onParams(params)

        self.initParam("Slide", params)
        self.initParam("Polygon", params)
        self.initParam("Current", params, 0)
        pass
    pass