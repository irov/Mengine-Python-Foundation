from Foundation.Object.DemonObject import DemonObject

class ObjectMovieEditBox(DemonObject):

    @staticmethod
    def declareORM(Type):
        DemonObject.declareORM(Type)
        Type.declareConst("ResourceMovieIdle")
        Type.declareConst("ResourceMovieOver")
        Type.declareConst("ResourceMovieFocus")
        Type.declareConst("ResourceMovieCarriage")
        Type.declareConst("ResourceMovieSlider")
        Type.declareConst("ResourceMovieBlock")

        Type.declareParam("Block")
        Type.declareParam("Value")
        Type.declareParam("Focus")
        Type.declareParam("PasswordChar")
        Type.declareParam("BlackList")
        Type.declareParam('Present')
        Type.declareParam('Text_ID')
        Type.declareParam('Text_Present_ID')
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
            '?',
            '1',
            '2',
            '3',
            '4',
            '5',
            '6',
            '7',
            '8',
            '9',
            '0'
        ])
        pass

    def setValueByDefault(self, value):
        entity = self.getEntity()
        entity.setValueByDefault(value)
        pass

    pass