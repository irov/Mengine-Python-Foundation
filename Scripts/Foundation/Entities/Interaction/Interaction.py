from Foundation.Entity.BaseEntity import BaseEntity
from Notification import Notification

class Interaction(BaseEntity):

    @staticmethod
    def declareORM(Type):
        BaseEntity.declareORM(Type)

        Type.addAction(Type, "Block")
        Type.addAction(Type, "Cursor")
        Type.addAction(Type, "Global", Update=Interaction.__updateGlobal)
        Type.addAction(Type, "Polygon", Update=Interaction.__updatePolygon)
        Type.addAction(Type, "HintPoint")
        Type.addAction(Type, "BlockKey")
        Type.addAction(Type, "Outward", Update=Interaction.__updateOutward)

    def __init__(self):
        super(Interaction, self).__init__()

        self.__hotspot = None
        self.__enableKeyEvent = False

    def __updatePolygon(self, value):
        hotspot = self.getHotSpot()

        if value is not None:
            hotspot.setPolygon(value)

    def __updateOutward(self, value):
        hotspot = self.getHotSpot()
        if hotspot is None:
            return

        hotspot.setOutward(value)

    def __updateGlobal(self, value):
        hotspot = self.getHotSpot()
        if hotspot is None:
            return

        hotspot.setGlobal(value)

    def _onInitialize(self, obj):
        super(Interaction, self)._onInitialize(obj)

        self.__hotspot = self._onCreateHotSpot()
        self.__hotspot.setEventListener(onHandleKeyEvent=self.__onKeyEvent,
                                        onHandleMouseButtonEvent=self._onMouseButtonEvent,
                                        onHandleMouseButtonEventEnd=self._onMouseButtonEventEnd,
                                        onHandleMouseButtonEventBegin=self._onMouseButtonEventBegin,
                                        onHandleMouseEnter=self._onMouseEnter,
                                        onHandleMouseLeave=self._onMouseLeave,
                                        onHandleMouseOverDestroy=self._onMouseOverDestroy)

    def _onFinalize(self):
        super(Interaction, self)._onFinalize()

        Mengine.destroyNode(self.__hotspot)
        self.__hotspot = None

    def _onCreateHotSpot(self):
        hotspot = self.createChild("HotSpotPolygon")

        name = self.object.getName()
        hotspot.setName(name)
        hotspot.enable()

        return hotspot

    def hasUniqueKeyEvent(self):
        return self._hasUniqueKeyEvent()

    def _hasUniqueKeyEvent(self):
        return False

    def getHotSpot(self):
        return self.__hotspot

    def _updateInteractive(self, value):
        BlockInteractive = self.object.getParam("BlockInteractive")

        if BlockInteractive is True:
            return

        hotspot = self.getHotSpot()

        if value is True:
            hotspot.enable()
            if self.__enableKeyEvent != value and self.hasUniqueKeyEvent() is False:
                hotspot.setEventListener(onHandleKeyEvent=self.__onKeyEvent)
        else:
            hotspot.disable()
            if self.__enableKeyEvent != value and self.hasUniqueKeyEvent() is False:
                hotspot.setEventListener(onHandleKeyEvent=None)

        self.__enableKeyEvent = value

    def __onKeyEvent(self, context, event):
        if self.__enableKeyEvent is False:
            return False

        result = self._keyEvent(context, event)

        return result

    def _keyEvent(self, context, event):
        return self.BlockKey

    def _updateBlockInteractive(self, value):
        if self.object.isInteractive() is False:
            return

        hotspot = self.getHotSpot()

        if value is True:
            hotspot.disable()
        else:
            hotspot.enable()

    def _onMouseEnter(self, context, event):
        Block = self.Block

        self._mouseEnter(event.x, event.y)

        return Block

    def _onMouseLeave(self, context, event):
        self._mouseLeave()

    def _onMouseOverDestroy(self):
        self._mouseLeave()

    def _onMouseButtonEventBegin(self, context, event):
        if event.button != 0:
            return False

        if event.isDown is True:
            self._mouseClickBegin(event.x, event.y)
        else:
            self._mouseClickUpBegin(event.x, event.y)

        return False

    def _onMouseButtonEvent(self, context, event):
        Block = self.Block

        if event.button != 0:
            return Block

        if event.isDown is True:
            self._mouseClick(event.x, event.y)
        else:
            self._mouseClickUp(event.x, event.y)

        return Block

    def _onMouseButtonEventEnd(self, context, event):
        if event.button != 0:
            return False

        if event.isDown is True:
            self._mouseClickEnd(event.x, event.y)
        else:
            self._mouseClickEndUp(event.x, event.y)

        return False

    def _mouseClickBegin(self, x, y):
        Notification.notify(Notificator.onInteractionClickBegin, self.object)

    def _mouseClick(self, x, y):
        Notification.notify(Notificator.onInteractionClick, self.object)

    def _mouseClickUpBegin(self, x, y):
        Notification.notify(Notificator.onInteractionClickUpBegin, self.object)

    def _mouseClickUp(self, x, y):
        Notification.notify(Notificator.onInteractionClickUp, self.object)

    def _mouseClickEnd(self, x, y):
        Notification.notify(Notificator.onInteractionClickEnd, self.object)

    def _mouseClickEndUp(self, x, y):
        Notification.notify(Notificator.onInteractionClickEndUp, self.object)

    def _mouseEnter(self, x, y):
        Notification.notify(Notificator.onInteractionMouseEnter, self.object)

    def _mouseLeave(self):
        Notification.notify(Notificator.onInteractionMouseLeave, self.object)

    def isMouseEnter(self):
        hotspot = self.getHotSpot()

        pickerOver = hotspot.isMousePickerOver()

        return pickerOver