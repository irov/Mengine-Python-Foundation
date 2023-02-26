from Foundation.Entity.BaseEntity import BaseEntity

class Point(BaseEntity):
    def __init__(self):
        super(Point, self).__init__()
        self.point = None
        pass

    def getPoint(self):
        return self.point
        pass

    def attach(self, entity):
        self.point.addChild(entity)
        pass

    def _onInitialize(self, obj):
        super(Point, self)._onInitialize(obj)

        self.point = self.createChild("Point")
        self.point.enable()
        pass

    def _onFinalize(self):
        super(Point, self)._onFinalize()

        Mengine.destroyNode(self.point)
        self.point = None
        pass
    pass