from Foundation.Manager import Manager

class LayerManager(Manager):
    s_LayerType = {}

    @staticmethod
    def importLayerType(module, name):
        Name = "%s" % (name)
        FromName = module
        ModuleName = "%s.%s" % (FromName, Name)
        Module = __import__(ModuleName, fromlist=[FromName])
        Type = getattr(Module, Name)

        LayerManager.s_LayerType[name] = Type
        pass

    @staticmethod
    def createLayer(name, params):
        Type = params.get("Type")

        if Type not in LayerManager.s_LayerType:
            return None

        LayerType = LayerManager.s_LayerType.get(Type)

        layer = LayerType()

        layer.setName(name)
        layer.onParams(params)

        return layer