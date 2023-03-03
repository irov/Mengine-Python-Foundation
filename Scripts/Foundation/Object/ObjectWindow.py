from Object import Object

class ObjectWindow(Object):
    @staticmethod
    def declareORM(Type):
        Object.declareORM(Type)

        Type.addResource(Type, "WindowResourceName")
        Type.addParam(Type, "Polygon")
        Type.addParam(Type, "ClientSize")

    def _onParams(self, params):
        super(ObjectWindow, self)._onParams(params)

        self.initResource("WindowResourceName", params, None)

        self.initParam("Polygon", params, None)
        self.initParam("ClientSize", params, None)
