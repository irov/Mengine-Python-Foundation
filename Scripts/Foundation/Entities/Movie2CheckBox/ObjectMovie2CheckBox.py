from Foundation.Object.DemonObject import DemonObject

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

        Type.addConst(Type, "CompositionNameTrue_Push")
        Type.addConst(Type, "CompositionNameTrue_Pressed")
        Type.addConst(Type, "CompositionNameTrue_Release")

        Type.addConst(Type, "CompositionNameFalse_Idle")
        Type.addConst(Type, "CompositionNameFalse_Enter")
        Type.addConst(Type, "CompositionNameFalse_Over")
        Type.addConst(Type, "CompositionNameFalse_Click")
        Type.addConst(Type, "CompositionNameFalse_Leave")

        Type.addConst(Type, "CompositionNameFalse_Push")
        Type.addConst(Type, "CompositionNameFalse_Pressed")
        Type.addConst(Type, "CompositionNameFalse_Release")

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
