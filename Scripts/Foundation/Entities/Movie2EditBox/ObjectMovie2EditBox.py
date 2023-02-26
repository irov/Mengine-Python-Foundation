from Foundation.Object.DemonObject import DemonObject

class ObjectMovie2EditBox(DemonObject):

    @staticmethod
    def declareORM(Type):
        DemonObject.declareORM(Type)
        Type.addConst(Type, "ResourceMovie")

        Type.addConst(Type, "CompositionNameIdle")
        Type.addConst(Type, "CompositionNameOver")
        Type.addConst(Type, "CompositionNameFocus")
        Type.addConst(Type, "CompositionNameCarriage")
        Type.addConst(Type, "CompositionNameSlider")
        Type.addConst(Type, "CompositionNameBlock")

        Type.addParam(Type, "Block")
        Type.addParam(Type, "Value")
        Type.addParam(Type, "Focus")
        Type.addParam(Type, "PasswordChar")
        Type.addParam(Type, "BlackList")
        Type.addParam(Type, 'Present')
        Type.addParam(Type, 'Text_ID')
        Type.addParam(Type, 'Text_Present_ID')
        Type.addParam(Type, 'TextLengthLimit')
        pass

    def _onParams(self, params):
        super(ObjectMovie2EditBox, self)._onParams(params)
        self.initConst("ResourceMovie", params)

        self.initConst("CompositionNameIdle", params)
        self.initConst("CompositionNameOver", params, None)
        self.initConst("CompositionNameFocus", params, None)
        self.initConst("CompositionNameCarriage", params, None)
        self.initConst("CompositionNameSlider", params, None)

        self.initConst("CompositionNameBlock", params, None)

        self.initParam("Block", params, False)
        self.initParam("TextLengthLimit", params, None)

        self.initParam("Value", params, u"")
        self.initParam("Present", params, u"Enter value")
        self.initParam("Text_ID", params, "ID_MovieEditBox")
        self.initParam("Text_Present_ID", params, "ID_MovieEditBox_Present")
        self.initParam("Focus", params, False)
        self.initParam("PasswordChar", params, None)
        self.initParam("BlackList", params, ['~', '`', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '+', '=', '}', '{', '[', ']', ':', ';', '\'', '\"', '\\', '|', '/', '>', '<', ',', '.', '?', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'])
        pass

    def setValueByDefault(self, value):
        entity = self.getEntity()
        entity.setValueByDefault(value)
        pass

    pass