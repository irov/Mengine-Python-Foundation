from Foundation.Entity.BaseEntity import BaseEntity

class Slider(BaseEntity):
    @staticmethod
    def declareORM(Type):
        BaseEntity.declareORM(Type)

        Type.addAction(Type, "Slide")
        Type.addAction(Type, "Polygon", Update=Slider._restorePolygon)
        Type.addAction(Type, "Current", Update=Slider._updateCurrent)
        pass

    def __init__(self):
        super(Slider, self).__init__()

        self.hotspot = None

        self.offset = None
        pass

    def _onInitialize(self, obj):
        super(Slider, self)._onInitialize(obj)

        self.hotspot = self.createChild("HotSpotPolygon")
        self.hotspot.enable()
        pass

    def _onFinalize(self):
        super(Slider, self)._onFinalize()

        Mengine.destroyNode(self.hotspot)
        self.hotspot = None
        pass

    def _onActivate(self):
        super(Slider, self)._onActivate()

        self.hotspot.setEventListener(onHandleMouseButtonEvent=self._onMouseButtonEvent)

        self.MouseButtonHandlerID = Mengine.addMouseButtonHandler(self.__onGlobalMouseButtonEvent)
        self.MouseMoveHandlerID = Mengine.addMouseMoveHandler(self.__onGlobalMouseMove)

        Mengine.enableGlobalHandler(self.MouseButtonHandlerID, False)
        Mengine.enableGlobalHandler(self.MouseMoveHandlerID, False)
        pass

    def _onDeactivate(self):
        super(Slider, self)._onDeactivate()

        self.hotspot.setEventListener(onHandleMouseButtonEvent=None)

        Mengine.removeGlobalHandler(self.MouseButtonHandlerID)
        Mengine.removeGlobalHandler(self.MouseMoveHandlerID)

        self.MouseButtonHandlerID = 0
        self.MouseMoveHandlerID = 0
        pass

    def _updateCurrent(self, value):
        x = self.Slide[1][0] - self.Slide[0][0]
        y = self.Slide[1][1] - self.Slide[0][1]
        pos = (self.Slide[0][0] + x * value, self.Slide[0][1] + y * value)

        self.object.setPosition(pos)
        pass

    def _restorePolygon(self, value):
        self.hotspot.setPolygon(value)
        pass

    def getHotSpot(self):
        return self.hotspot
        pass

    def _updateInteractive(self, value):
        if value is True:
            self.hotspot.enable()
        else:
            self.hotspot.disable()
            pass
        pass

    def __onGlobalMouseMove(self, event):
        arrowPos = Mengine.getCursorPosition()

        newPos = (arrowPos.x - self.offset[0], arrowPos.y - self.offset[1])
        newPos2 = Mengine.projectionPointToLine(newPos, self.Slide[0], self.Slide[1])

        self.object.setPosition((newPos2.x, newPos2.y))

        maxLength = Mengine.length_v2_v2(self.Slide[0], self.Slide[1])
        slideLength = Mengine.length_v2_v2(self.Slide[0], newPos2)

        current = slideLength / maxLength

        self.object.setParam("Current", current)

        Notification.notify(Notificator.onSlider, self.object, current)
        pass

    def __onGlobalMouseButtonEvent(self, event):
        if event.button != 0:
            return
            pass

        if event.isDown is False:
            Mengine.enableGlobalHandler(self.MouseButtonHandlerID, False)
            Mengine.enableGlobalHandler(self.MouseMoveHandlerID, False)

            Notification.notify(Notificator.onSliderUp, self.object)
            pass

        return
        pass

    def _onMouseButtonEvent(self, context, event):
        if event.button != 0:
            return False
            pass

        if event.isDown is True:
            Notification.notify(Notificator.onSliderDown, self.object)

            Mengine.enableGlobalHandler(self.MouseButtonHandlerID, True)
            Mengine.enableGlobalHandler(self.MouseMoveHandlerID, True)

            sliderPos = self.object.getPosition()

            self.offset = (event.position.world.x - sliderPos[0], event.position.world.y - sliderPos[1])
            pass

        return True
        pass
    pass