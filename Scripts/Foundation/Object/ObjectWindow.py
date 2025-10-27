from Object import Object

class ObjectWindow(Object):
    @staticmethod
    def declareORM(Type):
        Object.declareORM(Type)

        Type.declareResource("WindowResourceName")
        Type.declareParam("Polygon")
        Type.declareParam("ClientSize")

    def _onParams(self, params):
        super(ObjectWindow, self)._onParams(params)

        self.initResource("WindowResourceName", params, None)

        self.initParam("Polygon", params, None)
        self.initParam("ClientSize", params, None)
