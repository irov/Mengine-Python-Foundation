class Layer2D(object):
    __slots__ = "name", "node", "size"

    def __init__(self):
        self.name = None
        self.node = None
        self.size = (0.0, 0.0)
        pass

    def setName(self, name):
        self.name = name
        pass

    def getName(self):
        return self.name
        pass

    def onParams(self, params):
        self.size = params.get("Size", (0.0, 0.0))
        pass

    def createNode(self, scene):
        layer = scene.createChild("Layer2D")
        layer.setName(self.name)
        layer.setSize(self.size)
        layer.enable()

        self.node = layer

        return layer
        pass
    pass