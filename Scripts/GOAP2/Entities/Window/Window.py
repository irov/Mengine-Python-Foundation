from GOAP2.Entity.BaseEntity import BaseEntity

class Window(BaseEntity):
    @staticmethod
    def declareORM(Type):
        BaseEntity.declareORM(Type)

        Type.addAction(Type, "WindowResourceName")
        Type.addAction(Type, "Polygon")
        Type.addAction(Type, "ClientSize", Update=Window._updateClientSize)
        pass

    def __init__(self):
        super(Window, self).__init__()

        self.window = None
        pass

    def _updateClientSize(self, size):
        if size is None:
            return
            pass

        self.window.setClientSize(size)
        pass

    def _onInitialize(self, obj):
        super(Window, self)._onInitialize(obj)
        self.window = self.createChild("Window")

        self.window.setResourceWindow(self.WindowResourceName)
        self.window.enable()
        pass

    def _onFinalize(self):
        super(Window, self)._onFinalize()
        Menge.destroyNode(self.window)
        self.window = None
        pass
    pass