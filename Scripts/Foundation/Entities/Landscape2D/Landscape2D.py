from Foundation.Entity.BaseEntity import BaseEntity

class Landscape2D(BaseEntity):
    @staticmethod
    def declareORM(Type):
        BaseEntity.declareORM(Type)

        Type.addAction("ElementCountX")
        Type.addAction("ElementCountY")
        Type.addAction("ElementWidth")
        Type.addAction("ElementHeight")
        Type.addAction("BackParts")
        pass

    def __init__(self):
        super(Landscape2D, self).__init__()

        self.landscape2d = None
        pass

    # called by object db
    def _onInitialize(self, obj):
        super(Landscape2D, self)._onInitialize(obj)

        self.landscape2d = self.createChild("Landscape2D")

        name = self.getName()
        self.landscape2d.setName(name)
        self.landscape2d.setBackParts(self.BackParts, self.ElementCountX, self.ElementCountY, self.ElementWidth, self.ElementHeight)
        self.landscape2d.enable()
        pass

    # called by object db
    def _onFinalize(self):
        super(Landscape2D, self)._onFinalize()

        Mengine.destroyNode(self.landscape2d)
        self.landscape2d = None
        pass

    def getLandscape2D(self):
        return self.landscape2d
        pass
    pass