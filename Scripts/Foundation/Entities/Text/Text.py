from Foundation.Entity.BaseEntity import BaseEntity

class Text(BaseEntity):
    @staticmethod
    def declareORM(Type):
        BaseEntity.declareORM(Type)

        Type.addAction(Type, "TextID", Update=Text.__updateTextID)
        Type.addAction(Type, "TextArgs", Update=Text.__updateTextArgs)

        Type.addAction(Type, "Font", Update=Text.__updateFont)
        Type.addAction(Type, "FontRGBA", Update=Text.__updateFontRGBA)

        Type.addAction(Type, "LineOffset", Update=Text.__updateLineOffset)
        Type.addAction(Type, "CharOffset", Update=Text.__updateCharOffset)

        Type.addAction(Type, "MaxLength", Update=Text.__updateMaxLength)
        Type.addAction(Type, "MaxVisibleChar", Update=Text.__updateMaxVisibleChar)
        Type.addAction(Type, "Align", Update=Text.__updateAlign)
        Type.addAction(Type, "VerticalAlign", Update=Text.__updateVerticalAlign)
        Type.addAction(Type, "Pixelsnap", Update=Text.__updatePixelsnap)
        pass

    def __init__(self):
        super(Text, self).__init__()

        self.text_field = None
        pass

    def _onInitialize(self, obj):
        super(Text, self)._onInitialize(obj)
        self.text_field = self.createChild("TextField")

        name = self.getName()
        self.text_field.setName(name)

        self.text_field.enable()
        pass

    def _onFinalize(self):
        super(Text, self)._onFinalize()

        Mengine.destroyNode(self.text_field)
        self.text_field = None
        pass

    def __updatePixelsnap(self, value):
        self.text_field.setPixelsnap(value)
        pass

    def __updateLineOffset(self, offset):
        if offset is None:
            return
            pass

        self.text_field.setLineOffset(offset)
        pass

    def __updateCharOffset(self, offset):
        if offset is None:
            return
            pass

        self.text_field.setCharOffset(offset)
        pass

    def __updateTextID(self, textID):
        if textID is None:
            self.text_field.removeTextId()
            return
            pass

        self.text_field.setTextId(textID)
        pass

    def __updateTextArgs(self, args):
        if args is None:
            self.text_field.removeTextFormatArgs()
            return
            pass

        if isinstance(args, tuple) is True:
            self.text_field.setTextFormatArgs(*args)
        else:
            self.text_field.setTextFormatArgs(args)
            pass

        pass

    def __updateFont(self, font):
        if font is None:
            return
            pass

        self.text_field.setFontName(font)
        pass

    def __updateMaxLength(self, wrap):
        if wrap is None:
            self.text_field.setMaxLength(2048.0)
        else:
            maxlen = wrap[1][0] - wrap[0][0]
            self.text_field.setMaxLength(maxlen)
            pass
        pass

    def __updateMaxVisibleChar(self, value):
        if value is None:
            self.text_field.setMaxCharCount(-1)
        else:
            self.text_field.setMaxCharCount(value)
            pass
        pass

    def __updateAlign(self, align):
        if align == "None":
            pass
        elif align == "Left":
            self.text_field.setHorizontalLeftAlign()
            pass
        elif align == "Center":
            self.text_field.setHorizontalCenterAlign()
            pass
        elif align == "Right":
            self.text_field.setHorizontalRightAlign()
            pass
        else:
            Trace.log("Entity", 0, "Text.__updateAlign invalid align mode '%s'" % (align))
            pass
        pass

    def __updateVerticalAlign(self, align):
        if align == "None":
            pass
        elif align == "Bottom":
            self.text_field.setVerticalBottomAlign()
            pass
        elif align == "Center":
            self.text_field.setVerticalCenterAlign()
            pass
        elif align == "Top":
            self.text_field.setVerticalTopAlign()
            pass
        else:
            Trace.log("Entity", 0, "Text.__updateVerticalAlign invalid align mode '%s'" % (align))
            pass
        pass

    def getTextField(self):
        return self.text_field
        pass

    def getLength(self):
        return self.text_field.getTextSize()
        pass

    def __updateFontRGBA(self, rgba):
        if rgba is None:
            return
            pass

        self.text_field.setFontColor(rgba)
        pass

    pass