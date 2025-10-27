from Foundation.Object.Object import Object

class ObjectLandscape2D(Object):
    @staticmethod
    def declareORM(Type):
        Object.declareORM(Type)

        Type.declareConst("ElementCountX")
        Type.declareConst("ElementCountY")
        Type.declareConst("ElementWidth")
        Type.declareConst("ElementHeight")
        Type.declareConst("BackParts")
        pass

    def _onParams(self, params):
        super(ObjectLandscape2D, self)._onParams(params)

        self.initConst("ElementCountX", params, 0)
        self.initConst("ElementCountY", params, 0)
        self.initConst("ElementWidth", params, 0)
        self.initConst("ElementHeight", params, 0)

        partsResources = []

        BackParts = params.get("BackParts")

        for part in BackParts:
            resource = Mengine.getResourceReference(part)

            if resource is None:
                Trace.log("Object", 0, "ObjectLandscape2D._onParams: back parts %s invalid get" % (part))
                pass

            partsResources.append(resource)
            pass

        self.setConst("BackParts", partsResources)
        pass
    pass