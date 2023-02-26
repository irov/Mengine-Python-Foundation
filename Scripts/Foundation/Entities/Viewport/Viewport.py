from Foundation.Entity.BaseEntity import BaseEntity

class Viewport(BaseEntity):
    @staticmethod
    def declareORM(Type):
        BaseEntity.declareORM(Type)
        Type.addAction(Type, "Size")
        pass

    def _onActivate(self):
        layerGroup = self.object.getGroup()

        mainLayer = layerGroup.getMainLayer()
        mainLayer.setViewport(self.Size)
        pass
    pass