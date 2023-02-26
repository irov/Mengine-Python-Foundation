from DefaultNode import DefaultNode

class DefaultEntity(Mengine.Entity, DefaultNode):
    def __init__(self):
        super(DefaultEntity, self).__init__()

        self.cbMoveEnd = None
        self.cbRotateEnd = None
        self.cbScaleEnd = None
        self.cbColorEnd = None

        self.scene = None
        pass

    def setCbMoveEnd(self, fn):
        self.cbMoveEnd = fn
        pass

    def setCbColorEnd(self, fn):
        self.cbColorEnd = fn
        pass

    def setCbRotateEnd(self, fn):
        self.cbRotateEnd = fn
        pass

    def onMoveEnd(self):
        if self.cbMoveEnd != None:
            self.cbMoveEnd(self)

        pass

    def onRotateEnd(self):
        if self.cbRotateEnd != None:
            self.cbRotateEnd(self)

        pass

    def onColorEnd(self, node):
        if self.cbColorEnd != None:
            self.cbColorEnd(self)
        pass

    def setScene(self, scene):
        self.scene = scene
        pass

    def setCbScaleEnd(self, fn):
        self.cbScaleEnd = fn
        pass

    def onScaleEnd(self):
        if self.cbScaleEnd != None:
            self.cbScaleEnd(self)

        pass
    pass