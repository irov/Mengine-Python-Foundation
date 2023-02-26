from Foundation.Object.DemonObject import DemonObject

class ObjectProgressBar(DemonObject):

    @staticmethod
    def declareORM(Type):
        DemonObject.declareORM(Type)
        Type.addParam(Type, "Value")
        Type.addConst(Type, "MaxValue")
        Type.addConst(Type, "ResourceMovieProgress")
        pass

    def _onParams(self, params):
        super(ObjectProgressBar, self)._onParams(params)
        self.initParam("Value", params, 0)
        self.initConst("MaxValue", params, 150)
        self.initConst("ResourceMovieProgress", params)
        pass
    pass