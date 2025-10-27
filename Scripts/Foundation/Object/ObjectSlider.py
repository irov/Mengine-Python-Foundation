from DemonObject import DemonObject

class ObjectSlider(DemonObject):
    PARAMS_Interactive = 1

    @staticmethod
    def declareORM(Type):
        DemonObject.declareORM(Type)

        Type.declareParam("Slide")
        Type.declareParam("Polygon")
        Type.declareParam("Current")
        pass

    def _onParams(self, params):
        super(ObjectSlider, self)._onParams(params)

        self.initParam("Slide", params)
        self.initParam("Polygon", params)
        self.initParam("Current", params, 0)
        pass
    pass