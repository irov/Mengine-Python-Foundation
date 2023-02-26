from Foundation.Object.ObjectInteraction import ObjectInteraction

class ObjectButton(ObjectInteraction):
    @staticmethod
    def declareORM(Type):
        ObjectInteraction.declareORM(Type)

        Type.addParam(Type, "Font")
        Type.addParam(Type, "FontRGBA")

        Type.addParam(Type, "TextID")
        Type.addParam(Type, "TextArgs")

        Type.addParam(Type, "TextPosition")
        Type.addParam(Type, "TextPositionDown")
        Type.addParam(Type, "TextPositionOver")
        Type.addParam(Type, "TextAlign")
        Type.addParam(Type, "TextVerticalAlign")
        Type.addParam(Type, "TextLineOffset")

        Type.addParam(Type, "onUp")
        Type.addParam(Type, "onOver")
        Type.addParam(Type, "onDown")

        Type.addParam(Type, "KeyTag")
        Type.addParam(Type, "SoundTag")
        Type.addParam(Type, "SoundTagEnter")

        Type.addParam(Type, "BlockKeys")
        Type.addParam(Type, "BlockState")

    def _onParams(self, params):
        super(ObjectButton, self)._onParams(params)

        self.initParam("Font", params, None)
        self.initParam("FontRGBA", params, None)

        self.initParam("TextID", params, None)
        self.initParam("TextArgs", params, None)

        self.initParam("TextPosition", params, None)
        self.initParam("TextPositionDown", params, None)
        self.initParam("TextPositionOver", params, None)
        self.initParam("TextAlign", params, "Center")
        self.initParam("TextVerticalAlign", params, "Center")

        self.initConst("onUp", params)
        self.initConst("onOver", params)
        self.initConst("onDown", params)

        self.initParam("KeyTag", params, None)
        self.initParam("SoundTag", params, "ButtonClickDefault")
        self.initParam("SoundTagEnter", params, "ButtonEnterDefault")

        self.initParam("BlockKeys", params, False)
        self.initParam("BlockState", params, False)

    def _onInitialize(self):
        super(ObjectButton, self)._onInitialize()

        if _DEVELOPMENT is True:
            Font = self.getFont()
            if Font is not None:
                if Menge.hasFont(Font) is False:
                    self.initializeFailed("Font %s not found" % (Font))

    def setState(self, value):
        entity = self.getEntity()
        entity.setState(value)

    def getState(self):
        entity = self.getEntity()
        return entity.getState()