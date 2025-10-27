from Foundation.Object.ObjectInteraction import ObjectInteraction

class ObjectButton(ObjectInteraction):
    @staticmethod
    def declareORM(Type):
        ObjectInteraction.declareORM(Type)

        Type.declareParam("Font")
        Type.declareParam("FontRGBA")

        Type.declareParam("TextID")
        Type.declareParam("TextArgs")

        Type.declareParam("TextPosition")
        Type.declareParam("TextPositionDown")
        Type.declareParam("TextPositionOver")
        Type.declareParam("TextAlign")
        Type.declareParam("TextVerticalAlign")
        Type.declareParam("TextLineOffset")

        Type.declareParam("onUp")
        Type.declareParam("onOver")
        Type.declareParam("onDown")

        Type.declareParam("KeyTag")
        Type.declareParam("SoundTag")
        Type.declareParam("SoundTagEnter")

        Type.declareParam("BlockKeys")
        Type.declareParam("BlockState")

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
                if Mengine.hasFont(Font) is False:
                    self.initializeFailed("Font %s not found" % (Font))

    def setState(self, value):
        entity = self.getEntity()
        entity.setState(value)

    def getState(self):
        entity = self.getEntity()
        return entity.getState()