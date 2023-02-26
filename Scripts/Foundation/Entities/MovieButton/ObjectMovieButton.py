from Foundation.Object.DemonObject import DemonObject

class ObjectMovieButton(DemonObject):
    @staticmethod
    def declareORM(Type):
        DemonObject.declareORM(Type)
        Type.addConst(Type, "ResourceMovieIdle")
        Type.addConst(Type, "ResourceMovieEnter")
        Type.addConst(Type, "ResourceMovieOver")
        Type.addConst(Type, "ResourceMovieClick")
        Type.addConst(Type, "ResourceMovieLeave")

        Type.addConst(Type, "ResourceMoviePush")
        Type.addConst(Type, "ResourceMoviePressed")
        Type.addConst(Type, "ResourceMovieRelease")

        Type.addConst(Type, "ResourceMovieBlock")

        Type.addParam(Type, "Block")
        pass

    def _onParams(self, params):
        super(ObjectMovieButton, self)._onParams(params)
        self.initConst("ResourceMovieIdle", params)
        self.initConst("ResourceMovieEnter", params, None)
        self.initConst("ResourceMovieOver", params, None)
        self.initConst("ResourceMovieClick", params, None)
        self.initConst("ResourceMovieLeave", params, None)

        self.initConst("ResourceMoviePush", params, None)
        self.initConst("ResourceMoviePressed", params, None)
        self.initConst("ResourceMovieRelease", params, None)

        self.initConst("ResourceMovieBlock", params, None)

        self.initParam("Block", params, False)
        pass

    def setupMoviesTextArguments(self, TextName, *Args):
        if self.isActive() is False:
            return False

        Entity = self.getEntity()

        for Movie in Entity.Movies.itervalues():
            if Movie.setupMovieTextArguments(TextName, *Args) is False:
                return False

        return True

    def eachMovies(self):
        if self.isActive() is not False:
            Entity = self.getEntity()

            for Movie in Entity.Movies.itervalues():
                yield Movie

    def getCurrentMovieSocketCenter(self):
        entity = self.getEntity()

        if entity is not None:
            return entity.getCurrentMovieSocketCenter()