from Object import Object

class ObjectViewport(Object):
    @staticmethod
    def declareORM(Type):
        Object.declareORM(Type)

        Type.addParam(Type, "Size")

    def _onParams(self, params):
        super(ObjectViewport, self)._onParams(params)
        self.initParam("Size", params, None)

    def _onInitialize(self):
        super(ObjectViewport, self)._onInitialize()

        if _DEVELOPMENT is True:
            Size = self.getSize()
            if Size is None:
                self.initializeFailed("'%s' invalid initialize, incorrect param Size" % (self.getName()))
