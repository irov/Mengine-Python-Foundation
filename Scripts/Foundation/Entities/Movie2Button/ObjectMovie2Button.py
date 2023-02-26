from Foundation.Object.DemonObject import DemonObject

class ObjectMovie2Button(DemonObject):
    @staticmethod
    def declareORM(Type):
        DemonObject.declareORM(Type)
        Type.addConst(Type, "ResourceMovie")
        Type.addConst(Type, "CompositionNameIdle")
        Type.addConst(Type, "CompositionNameAppear")
        Type.addConst(Type, "CompositionNameEnter")
        Type.addConst(Type, "CompositionNameOver")
        Type.addConst(Type, "CompositionNameClick")
        Type.addConst(Type, "CompositionNameLeave")

        Type.addConst(Type, "CompositionNamePush")
        Type.addConst(Type, "CompositionNamePressed")
        Type.addConst(Type, "CompositionNameRelease")

        Type.addConst(Type, "CompositionNameBlock")
        Type.addConst(Type, "CompositionNameBlockEnd")
        Type.addConst(Type, "CompositionNameBlockEnter")

        Type.addConst(Type, "CompositionNameSelected")
        Type.addConst(Type, "CompositionNameSelectedEnd")
        Type.addConst(Type, "CompositionNameSelectedEnter")

        Type.addParam(Type, "Block")
        Type.addParam(Type, "Selected")

        Type.addParam(Type, "KeyTag")
        Type.addParam(Type, "BlockKeys")
        Type.addParam(Type, "Synchronize")
        pass

    def _onParams(self, params):
        super(ObjectMovie2Button, self)._onParams(params)
        self.initConst("ResourceMovie", params, None)

        self.initConst("CompositionNameIdle", params)
        self.initConst("CompositionNameAppear", params, None)
        self.initConst("CompositionNameEnter", params, None)
        self.initConst("CompositionNameOver", params, None)
        self.initConst("CompositionNameClick", params, None)
        self.initConst("CompositionNameLeave", params, None)

        self.initConst("CompositionNamePush", params, None)
        self.initConst("CompositionNamePressed", params, None)
        self.initConst("CompositionNameRelease", params, None)

        self.initConst("CompositionNameBlock", params, None)
        self.initConst("CompositionNameBlockEnd", params, None)
        self.initConst("CompositionNameBlockEnter", params, None)

        self.initConst("CompositionNameSelected", params, None)
        self.initConst("CompositionNameSelectedEnd", params, None)
        self.initConst("CompositionNameSelectedEnter", params, None)

        self.initParam("Block", params, False)
        self.initParam("Selected", params, False)

        self.initParam("KeyTag", params, "False")

        self.initParam("BlockKeys", params, False)
        self.initParam("Synchronize", params, False)
        pass

    def hasSlot(self, slot_name):
        return self.getEntity().hasSlot(slot_name)

    def addChildToSlot(self, node, slot_name):
        return self.getEntity().addChildToSlot(node, slot_name)

    def removeFromParentSlot(self, node, slot_name):
        return self.getEntity().removeFromParentSlot(node, slot_name)

    def returnToParentFromSlot(self, entity, slot_name):
        return self.getEntity().returnToParentFromSlot(entity, slot_name)

    def getCompositionBounds(self):
        return self.getEntity().getCompositionBounds()

    def hasCompositionBounds(self):
        return self.getEntity().hasCompositionBounds()

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

    def setTextAliasEnvironment(self, env_name):
        for movie in self.eachMovies():
            movie.setTextAliasEnvironment(env_name)

    def getCurrentMovieSocketCenter(self):
        entity = self.getEntity()

        if entity is not None:
            return entity.getCurrentMovieSocketCenter()