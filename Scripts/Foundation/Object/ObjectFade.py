from DemonObject import DemonObject

class ObjectFade(DemonObject):
    @staticmethod
    def declareORM(Type):
        DemonObject.declareORM(Type)

        Type.declareParam("Size")

    def _onParams(self, params):
        super(ObjectFade, self)._onParams(params)

        self.initParam("Size", params, None)