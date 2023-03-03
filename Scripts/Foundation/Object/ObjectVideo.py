from Object import Object

class ObjectVideo(Object):
    @staticmethod
    def declareORM(Type):
        Object.declareORM(Type)

        Type.addResource(Type, "VideoResourceName")
        Type.addParam(Type, "Play")

    def _onParams(self, params):
        super(ObjectVideo, self)._onParams(params)

        self.initResource("VideoResourceName", params, None)
        self.initParam("Play", params, False)
