from Foundation.Object.DemonObject import DemonObject

class ObjectMovieButton(DemonObject):
    def _onParams(self, params):
        super(ObjectMovieButton, self)._onParams(params)
        self.initParam("IsAttachReact", params, False)
        self.initParam("HintPoint", params, None)

        self.initConst("ResourceMovieIdle", params)
        self.initConst("ResourceMovieEnter", params, None)
        self.initConst("ResourceMovieOver", params)
        self.initConst("ResourceMovieClick", params)
        self.initConst("ResourceMoviePressed", params, None)
        self.initConst("ResourceMovieRelease", params, None)
        self.initConst("ResourceMovieLeave", params, None)

        self.initParam("Clickable", params, None)

        self.initParam("KeyTag", params, None)
        self.initParam("BlockKeys", params, False)
        self.initParam("SwitchMode", params, False)
        self.initParam("Over", params, False)
        # self.initParam("Interactive", params, False)
        pass

    def calcWorldHintPoint(self):
        hintPoint = self.getHintPoint()

        if hintPoint is None:
            return None
            pass

        groupScene = self.getGroup()

        slot = groupScene.getScene()

        posScene = slot.getLocalPosition()

        pos = (posScene.x + hintPoint[0], posScene.y + hintPoint[1])

        return pos
        pass
    pass