# coding=UTF-8
from DefaultNode import DefaultNode

# ------------------------------------------------------------------------------
# Class: DefaultEntity
# Description:
# - 
# ------------------------------------------------------------------------------
class DefaultEntity(Menge.Entity, DefaultNode):
    # ----------------------------------------------------------------------------
    # Method: __init__
    # Description:
    # -
    # ----------------------------------------------------------------------------
    def __init__(self):
        super(DefaultEntity, self).__init__()

        self.cbMoveEnd = None
        self.cbRotateEnd = None
        self.cbScaleEnd = None
        self.cbColorEnd = None

        self.scene = None
        pass

    # ----------------------------------------------------------------------------
    # Method: setCbMoveEnd
    # Description:
    # -
    # ----------------------------------------------------------------------------
    def setCbMoveEnd(self, fn):
        self.cbMoveEnd = fn
        pass

    # ----------------------------------------------------------------------------
    # Method: setCbColorEnd
    # Description:
    # -
    # ----------------------------------------------------------------------------
    def setCbColorEnd(self, fn):
        self.cbColorEnd = fn
        pass

    # ----------------------------------------------------------------------------
    # Method: onRotateEnd
    # Description:
    # -
    # ----------------------------------------------------------------------------
    def setCbRotateEnd(self, fn):
        self.cbRotateEnd = fn
        pass

    # ----------------------------------------------------------------------------
    # Method: onMoveEnd
    # Description:
    # -
    # ----------------------------------------------------------------------------
    def onMoveEnd(self):
        if self.cbMoveEnd != None:
            self.cbMoveEnd(self)

        pass

    # ----------------------------------------------------------------------------
    # Method: onRotateEnd
    # Description:
    # -
    # ----------------------------------------------------------------------------
    def onRotateEnd(self):
        if self.cbRotateEnd != None:
            self.cbRotateEnd(self)

        pass

    # ----------------------------------------------------------------------------
    # Method: onColorEnd
    # Description:
    # -
    # ----------------------------------------------------------------------------
    def onColorEnd(self, node):
        if self.cbColorEnd != None:
            self.cbColorEnd(self)
        pass

    # ----------------------------------------------------------------------------
    # Method: setScene
    # Description:
    # -
    # ----------------------------------------------------------------------------
    def setScene(self, scene):
        self.scene = scene
        pass

    # ----------------------------------------------------------------------------
    # Method: setCbScaleEnd
    # Description:
    # -
    # ----------------------------------------------------------------------------
    def setCbScaleEnd(self, fn):
        self.cbScaleEnd = fn
        pass

    # ----------------------------------------------------------------------------
    # Method: onScaleEnd
    # Description:
    # -
    # ----------------------------------------------------------------------------
    def onScaleEnd(self):
        if self.cbScaleEnd != None:
            self.cbScaleEnd(self)

        pass
    pass