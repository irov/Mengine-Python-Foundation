from DemonObject import DemonObject

class ObjectEditBox(DemonObject):
    @staticmethod
    def declareORM(Type):
        DemonObject.declareORM(Type)

        Type.addParam(Type, "Polygon")
        Type.addParam(Type, "Wrap")
        Type.addParam(Type, "Value")
        Type.addParam(Type, "Focus")
        Type.addParam(Type, "PasswordChar")
        Type.addParam(Type, "BlackList")
        Type.addParam(Type, "TextLengthLimit")
        pass

    def _onParams(self, params):
        super(ObjectEditBox, self)._onParams(params)

        self.initParam("Polygon", params, None)
        self.initParam("TextLengthLimit", params, None)
        self.initParam("Wrap", params)
        self.initParam("Value", params, u"")
        self.initParam("Focus", params, True)
        self.initParam("PasswordChar", params, None)
        self.initParam("BlackList", params, ['~', '`', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '+', '=', '}', '{', '[', ']', ':', ';', '\'', '\"', '\\', '|', '/', '>', '<', ',', '.', '?'  # , '1'
            # , '2'
            # , '3'
            # , '4'
            # , '5'
            # , '6'
            # , '7'
            # , '8'
            # , '9'
            # , '0'
        ])