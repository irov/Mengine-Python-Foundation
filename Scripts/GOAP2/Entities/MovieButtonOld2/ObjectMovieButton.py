from GOAP2.Object.DemonObject import DemonObject

class ObjectMovieButton(DemonObject):
    @staticmethod
    def declareORM(Type):
        DemonObject.declareORM(Type)
        Type.addConst(Type, "ResourceMovieIdle")
        Type.addConst(Type, "ResourceMovieEnter")
        Type.addConst(Type, "ResourceMovieOver")
        Type.addConst(Type, "ResourceMovieClick")
        Type.addConst(Type, "ResourceMoviePressed")
        Type.addConst(Type, "ResourceMoviePush")
        Type.addConst(Type, "ResourceMovieRelease")
        Type.addConst(Type, "ResourceMovieLeave")

        Type.addParam(Type, "KeyTag")
        Type.addParam(Type, "BlockKeys")
        Type.addParam(Type, "Block")
        Type.addParam(Type, "TextFont")
        Type.addParam(Type, "TextAlign")
        Type.addParam(Type, "TextVerticalAlign")
        Type.addParam(Type, "TextArgs")
        pass

    def _onParams(self, params):
        super(ObjectMovieButton, self)._onParams(params)
        self.initConst("ResourceMovieIdle", params)
        self.initConst("ResourceMovieEnter", params, None)
        self.initConst("ResourceMovieOver", params)
        self.initConst("ResourceMovieClick", params)
        self.initConst("ResourceMoviePressed", params, None)
        self.initConst("ResourceMovieRelease", params, None)
        self.initConst("ResourceMovieLeave", params, None)
        self.initConst("ResourceMoviePush", params, None)

        self.initParam("KeyTag", params, None)
        self.initParam("BlockKeys", params, False)
        self.initParam("Block", params, True)
        self.initParam("TextFont", params, None)
        self.initParam("TextAlign", params, None)
        self.initParam("TextVerticalAlign", params, None)
        self.initParam("TextArgs", params, None)
        pass

    pass