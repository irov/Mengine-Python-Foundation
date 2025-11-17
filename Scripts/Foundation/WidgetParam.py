class WidgetParam(object):
    def __init__(self, Type, ReadOnly, Description, Step):
        self.Type = Type
        self.ReadOnly = ReadOnly
        self.Description = Description
        self.Step = 0.0 if Step is None else Step
        pass

    def getType(self):
        return self.Type

    def isReadOnly(self):
        return self.ReadOnly

    def getDescription(self):
        return self.Description

    def getStep(self):
        return self.Step
    pass

class WidgetParamCheckBox(WidgetParam):
    def __init__(self, ReadOnly=False, Description=None, Step=None):
        super(WidgetParamCheckBox, self).__init__(Mengine.LEWT_CHECKBOX, ReadOnly, Description, Step)
        pass
    pass

class WidgetParamPosition(WidgetParam):
    def __init__(self,  ReadOnly=False, Description=None, Step=0.001):
        super(WidgetParamPosition, self).__init__(Mengine.LEWT_POSITION, ReadOnly, Description, Step)
        pass
    pass

class WidgetParamScale(WidgetParam):
    def __init__(self, ReadOnly=False, Description=None, Step=0.001):
        super(WidgetParamScale, self).__init__(Mengine.LEWT_SCALE, ReadOnly, Description, Step)
        pass
    pass

class WidgetParamOrientation(WidgetParam):
    def __init__(self, ReadOnly=False, Description=None, Step=0.0174533):
        super(WidgetParamOrientation, self).__init__(Mengine.LEWT_ORIENTATION, ReadOnly, Description, Step)
        pass
    pass

class WidgetParamAlpha(WidgetParam):
    def __init__(self, ReadOnly=False, Description=None, Step=0.01):
        super(WidgetParamAlpha, self).__init__(Mengine.LEWT_ALPHA, ReadOnly, Description, Step)
        pass
    pass

class WidgetParamRGB(WidgetParam):
    def __init__(self, ReadOnly=False, Description=None, Step=0.01):
        super(WidgetParamRGB, self).__init__(Mengine.LEWT_RGB, ReadOnly, Description, Step)
        pass
    pass