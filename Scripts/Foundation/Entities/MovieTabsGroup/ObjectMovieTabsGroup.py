from Foundation.Object.DemonObject import DemonObject

class ObjectMovieTabsGroup(DemonObject):
    @staticmethod
    def declareORM(Type):
        DemonObject.declareORM(Type)
        Type.addConst(Type, "Tabs")
        Type.addParam(Type, "Choice")
        pass

    def _onParams(self, params):
        super(ObjectMovieTabsGroup, self)._onParams(params)
        self.initConst("Tabs", params)
        self.initParam('Choice', params, None)
        pass

    pass