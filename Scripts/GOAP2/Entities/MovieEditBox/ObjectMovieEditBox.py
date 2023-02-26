from GOAP2.Object.DemonObject import DemonObject

class ObjectMovieEditBox(DemonObject):

    @staticmethod
    def declareORM(Type):
        DemonObject.declareORM(Type)
        Type.addConst(Type, "ResourceMovieIdle")
        Type.addConst(Type, "ResourceMovieOver")
        Type.addConst(Type, "ResourceMovieFocus")
        Type.addConst(Type, "ResourceMovieCarriage")
        Type.addConst(Type, "ResourceMovieSlider")
        Type.addConst(Type, "ResourceMovieBlock")

        Type.addParam(Type, "Block")
        Type.addParam(Type, "Value")
        Type.addParam(Type, "Focus")
        Type.addParam(Type, "PasswordChar")
        Type.addParam(Type, "BlackList")
        Type.addParam(Type, 'Present')
        Type.addParam(Type, 'Text_ID')
        Type.addParam(Type, 'Text_Present_ID')
        pass

    def _onParams(self, params):
        super(ObjectMovieEditBox, self)._onParams(params)
        self.initConst("ResourceMovieIdle", params)
        self.initConst("ResourceMovieOver", params, None)
        self.initConst("ResourceMovieFocus", params, None)
        self.initConst("ResourceMovieCarriage", params, None)
        self.initConst("ResourceMovieSlider", params, None)

        self.initConst("ResourceMovieBlock", params, None)

        self.initParam("Block", params, False)

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