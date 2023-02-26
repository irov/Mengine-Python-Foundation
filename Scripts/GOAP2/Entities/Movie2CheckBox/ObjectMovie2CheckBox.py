from GOAP2.Object.DemonObject import DemonObject

class ObjectMovie2CheckBox(DemonObject):

    @staticmethod
    def declareORM(Type):
        DemonObject.declareORM(Type)
        Type.addParam(Type, "Value")

        Type.addConst(Type, "ResourceMovie")

        Type.addConst(Type, "CompositionNameTrue_Idle")
        Type.addConst(Type, "CompositionNameTrue_Enter")
        Type.addConst(Type, "CompositionNameTrue_Over")
        Type.addConst(Type, "CompositionNameTrue_Click")
        Type.addConst(Type, "CompositionNameTrue_Leave")

        Type.addConst(Type, "CompositionNameFalse_Idle")
        Type.addConst(Type, "CompositionNameFalse_Enter")
        Type.addConst(Type, "CompositionNameFalse_Over")
        Type.addConst(Type, "CompositionNameFalse_Click")
        Type.addConst(Type, "CompositionNameFalse_Leave")

        Type.addParam(Type, "BlockState")
        pass

    def _onParams(self, params):
        super(ObjectMovie2CheckBox, self)._onParams(params)
        self.initParam("Value", params, False)

        self.initConst("ResourceMovie", params)

        self.initConst("CompositionNameTrue_Idle", params)
        self.initConst("CompositionNameTrue_Enter", params, None)
        self.initConst("CompositionNameTrue_Over", params, None)
        self.initConst("CompositionNameTrue_Click", params, None)
        self.initConst("CompositionNameTrue_Leave", params, None)

        self.initConst("CompositionNameFalse_Idle", params, None)
        self.initConst("CompositionNameFalse_Enter", params, None)
        self.initConst("CompositionNameFalse_Over", params, None)
        self.initConst("CompositionNameFalse_Click", params, None)
        self.initConst("CompositionNameFalse_Leave", params, None)

        self.initParam("BlockState", params, False)
        pass

    def getCurrentMovieSocketCenter(self):
        entity = self.getEntity()

        if entity is not None:
            button_false = entity.MovieButtonFalse
            button_true = entity.MovieButtonTrue

            current_button = button_false if button_false.getEnable() else button_true

            return current_button.getCurrentMovieSocketCenter()