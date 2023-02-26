from DemonObject import DemonObject

class ObjectFade(DemonObject):
    @staticmethod
    def declareORM(Type):
        DemonObject.declareORM(Type)

        Type.addParam(Type, "Size")

    def _onParams(self, params):
        super(ObjectFade, self)._onParams(params)

        self.initParam("Size", params, None)