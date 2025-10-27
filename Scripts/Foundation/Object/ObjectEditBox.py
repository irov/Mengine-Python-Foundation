from DemonObject import DemonObject

class ObjectEditBox(DemonObject):
    @staticmethod
    def declareORM(Type):
        DemonObject.declareORM(Type)

        Type.declareParam("Polygon")
        Type.declareParam("Wrap")
        Type.declareParam("Value")
        Type.declareParam("Focus")
        Type.declareParam("PasswordChar")
        Type.declareParam("BlackList")
        Type.declareParam("TextLengthLimit")
        pass

    def _onParams(self, params):
        super(ObjectEditBox, self)._onParams(params)

        self.initParam("Polygon", params, None)
        self.initParam("TextLengthLimit", params, None)
        self.initParam("Wrap", params)
        self.initParam("Value", params, u"")
        self.initParam("Focus", params, True)
        self.initParam("PasswordChar", params, None)
        self.initParam("BlackList", params, [
            '~',
            '`',
            '!',
            '@',
            '#',
            '$',
            '%',
            '^',
            '&',
            '*',
            '(',
            ')',
            '-',
            '+',
            '=',
            '}',
            '{',
            '[',
            ']',
            ':',
            ';',
            '\'',
            '\"',
            '\\',
            '|',
            '/',
            '>',
            '<',
            ',',
            '.',
            '?'  # ,
            '1'
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