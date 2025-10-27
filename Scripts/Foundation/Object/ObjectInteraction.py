from Object import Object

class ObjectInteraction(Object):
    @staticmethod
    def declareORM(Type):
        Object.declareORM(Type)

        Type.declareConst("Polygon")
        Type.declareConst("HintPoint")
        Type.declareParam("Block", bool)
        Type.declareParam("BlockKey")
        Type.declareParam("Cursor")
        Type.declareParam("Outward", bool)
        Type.declareParam("Global", bool)
        pass

    def __init__(self):
        super(ObjectInteraction, self).__init__()
        pass

    def _onParams(self, params):
        super(ObjectInteraction, self)._onParams(params)

        self.initConst("Polygon", params, None)
        self.initConst("HintPoint", params, None)
        self.initParam("Block", params, True)
        self.initParam("BlockKey", params, False)
        self.initParam("Cursor", params, None)
        self.initParam("Outward", params, False)
        self.initParam("Global", params, False)
        pass

    def _onInitialize(self):
        super(ObjectInteraction, self)._onInitialize()
        HintPoint = self.getHintPoint()

        if _DEVELOPMENT is True:
            if HintPoint is not None:
                if isinstance(HintPoint, tuple) is False or len(HintPoint) != 2:
                    self.initializeFailed("'%s' invalid initialize, incorrect param HintPoint" % (self.getName()))

                Polygon = self.getPolygon()
                if Polygon is not None and len(Polygon) != 0:
                    if Mengine.isPointInsidePolygon(HintPoint, Polygon) is False:
                        self.initializeFailed("[%s] '%s' invalid initialize, HintPoint %s must be inside polygon %s" % (self.getParent().getName(), self.getName(), HintPoint, Polygon))

        if self.getType() == "ObjectItem":
            return

        if _DEVELOPMENT is True:
            if self.getGlobal() is False:
                Polygon = self.getPolygon()

                if Polygon is None:
                    self.initializeFailed("ObjectInteraction invalid initialize, incorrect param Polygon (None)")
                    pass

                if len(Polygon) == 0:
                    self.initializeFailed("ObjectInteraction invalid initialize, incorrect param Polygon (Zero)")
                    pass
                pass
            pass
        pass

    def calcWorldHintPoint(self):
        hintPoint = self.getHintPoint()

        if hintPoint is not None:
            groupScene = self.getGroup()
            slot = groupScene.getScene()
            posScene = slot.getLocalPosition()

            return posScene.x + hintPoint[0], posScene.y + hintPoint[1]

        if self.isActive():
            hotspot = self.entity.getHotSpot()

            if hotspot is not None:
                if hotspot.__class__.__name__ == "HotSpotPolygon":
                    return hotspot.getWorldPolygonCenter()

                elif hotspot.__class__.__name__ == "HotSpotImage":
                    pos = hotspot.getWorldPosition()

                    pos.x += hotspot.getWidth() >> 1
                    pos.y += hotspot.getHeight() >> 1

                    return pos