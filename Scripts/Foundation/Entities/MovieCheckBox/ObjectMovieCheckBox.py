from Foundation.Object.DemonObject import DemonObject

class ObjectMovieCheckBox(DemonObject):

    @staticmethod
    def declareORM(Type):
        DemonObject.declareORM(Type)
        Type.declareParam("Value")

        Type.declareConst("ResourceMovieTrue_Idle")
        Type.declareConst("ResourceMovieTrue_Enter")
        Type.declareConst("ResourceMovieTrue_Over")
        Type.declareConst("ResourceMovieTrue_Click")
        Type.declareConst("ResourceMovieTrue_Leave")

        Type.declareConst("ResourceMovieFalse_Idle")
        Type.declareConst("ResourceMovieFalse_Enter")
        Type.declareConst("ResourceMovieFalse_Over")
        Type.declareConst("ResourceMovieFalse_Click")
        Type.declareConst("ResourceMovieFalse_Leave")

        Type.declareParam("BlockState")
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