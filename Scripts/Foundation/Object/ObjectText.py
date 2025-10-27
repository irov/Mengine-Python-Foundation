from Object import Object

class ObjectText(Object):
    @staticmethod
    def declareORM(Type):
        Object.declareORM(Type)

        Type.declareParam("Font")
        Type.declareParam("TextID")
        Type.declareParam("TextArgs")
        Type.declareParam("FontRGBA")
        Type.declareParam("LineOffset")
        Type.declareParam("CharOffset")
        Type.declareParam("MaxLength")
        Type.declareParam("MaxVisibleChar")
        Type.declareParam("Align")
        Type.declareParam("VerticalAlign")
        Type.declareParam("Pixelsnap")

    def _onParams(self, params):
        super(ObjectText, self)._onParams(params)

        self.initParam("Font", params, None)
        self.initParam("FontRGBA", params, None)

        self.initParam("TextID", params, None)
        self.initParam("TextArgs", params, None)

        self.initParam("LineOffset", params, None)
        self.initParam("CharOffset", params, None)

        self.initParam("MaxLength", params, None)
        self.initParam("MaxVisibleChar", params, None)
        self.initParam("Align", params, "None")
        self.initParam("VerticalAlign", params, "None")
        self.initParam("Pixelsnap", params, False)

    def _onInitialize(self):
        super(ObjectText, self)._onInitialize()

        if _DEVELOPMENT is True:
            Font = self.getFont()
            if Font is not None:
                if Mengine.hasFont(Font) is False:
                    self.initializeFailed("Font %s not found" % (Font))