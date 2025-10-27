from Foundation.Object.DemonObject import DemonObject

class ObjectMovie2CheckBox(DemonObject):

    @staticmethod
    def declareORM(Type):
        DemonObject.declareORM(Type)
        Type.declareParam("Value")

        Type.declareConst("ResourceMovie")

        Type.declareConst("CompositionNameTrue_Idle")
        Type.declareConst("CompositionNameTrue_Enter")
        Type.declareConst("CompositionNameTrue_Over")
        Type.declareConst("CompositionNameTrue_Click")
        Type.declareConst("CompositionNameTrue_Leave")

        Type.declareConst("CompositionNameTrue_Push")
        Type.declareConst("CompositionNameTrue_Pressed")
        Type.declareConst("CompositionNameTrue_Release")

        Type.declareConst("CompositionNameFalse_Idle")
        Type.declareConst("CompositionNameFalse_Enter")
        Type.declareConst("CompositionNameFalse_Over")
        Type.declareConst("CompositionNameFalse_Click")
        Type.declareConst("CompositionNameFalse_Leave")

        Type.declareConst("CompositionNameFalse_Push")
        Type.declareConst("CompositionNameFalse_Pressed")
        Type.declareConst("CompositionNameFalse_Release")

        Type.declareParam("BlockState")
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

        self.initConst("CompositionNameTrue_Push", params, None)
        self.initConst("CompositionNameTrue_Pressed", params, None)
        self.initConst("CompositionNameTrue_Release", params, None)

        self.initConst("CompositionNameFalse_Idle", params, None)
        self.initConst("CompositionNameFalse_Enter", params, None)
        self.initConst("CompositionNameFalse_Over", params, None)
        self.initConst("CompositionNameFalse_Click", params, None)
        self.initConst("CompositionNameFalse_Leave", params, None)

        self.initConst("CompositionNameFalse_Push", params, None)
        self.initConst("CompositionNameFalse_Pressed", params, None)
        self.initConst("CompositionNameFalse_Release", params, None)

        self.initParam("BlockState", params, False)
        pass

    def getCurrentMovieSocketCenter(self):
        return self.getEntity().getCurrentMovieSocketCenter()

    def getCompositionBounds(self):
        return self.getEntity().getCompositionBounds()

    def hasCompositionBounds(self):
        return self.getEntity().hasCompositionBounds()

    def addChildToSlot(self, node, slot_name):
        return self.getEntity().addChildToSlot(node, slot_name)

    def setTextAliasEnvironment(self, env_name):
        return self.getEntity().setTextAliasEnvironment(env_name)
