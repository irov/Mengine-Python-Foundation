from GOAP2.Object.DemonObject import DemonObject

class ObjectMovieCheckBox(DemonObject):

    @staticmethod
    def declareORM(Type):
        DemonObject.declareORM(Type)
        Type.addParam(Type, "Value")

        Type.addConst(Type, "ResourceMovieTrue_Idle")
        Type.addConst(Type, "ResourceMovieTrue_Enter")
        Type.addConst(Type, "ResourceMovieTrue_Over")
        Type.addConst(Type, "ResourceMovieTrue_Click")
        Type.addConst(Type, "ResourceMovieTrue_Leave")

        Type.addConst(Type, "ResourceMovieFalse_Idle")
        Type.addConst(Type, "ResourceMovieFalse_Enter")
        Type.addConst(Type, "ResourceMovieFalse_Over")
        Type.addConst(Type, "ResourceMovieFalse_Click")
        Type.addConst(Type, "ResourceMovieFalse_Leave")

        Type.addParam(Type, "BlockState")
        pass

    def _onParams(self, params):
        super(ObjectMovieCheckBox, self)._onParams(params)
        self.initParam("Value", params, False)
        self.initConst("ResourceMovieTrue_Idle", params)
        self.initConst("ResourceMovieTrue_Enter", params)
        self.initConst("ResourceMovieTrue_Over", params)
        self.initConst("ResourceMovieTrue_Click", params)
        self.initConst("ResourceMovieTrue_Leave", params)

        self.initConst("ResourceMovieFalse_Idle", params)
        self.initConst("ResourceMovieFalse_Enter", params)
        self.initConst("ResourceMovieFalse_Over", params)
        self.initConst("ResourceMovieFalse_Click", params)
        self.initConst("ResourceMovieFalse_Leave", params)

        self.initParam("BlockState", params, False)
        pass

    def getCurrentMovieSocketCenter(self):
        entity = self.getEntity()

        if entity is not None:
            button_false = entity.MovieButtonFalse
            button_true = entity.MovieButtonTrue

            current_button = button_false if button_false.getEnable() else button_true

            return current_button.getCurrentMovieSocketCenter()