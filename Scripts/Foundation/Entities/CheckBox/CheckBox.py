from Foundation.Entity.BaseEntity import BaseEntity

from Notification import Notification

class CheckBox(BaseEntity):
    s_keys = dict(Esc=Menge.KC_ESCAPE, Enter=Menge.KC_RETURN)

    @staticmethod
    def declareORM(Type):
        BaseEntity.declareORM(Type)

        Type.addAction(Type, "Polygon", Update=CheckBox._restorePolygon)
        Type.addAction(Type, "State", Update=CheckBox._updateState)
        Type.addAction(Type, "BlockState", Update=CheckBox._updateState)
        Type.addAction(Type, "KeyTag")
        pass

    def __init__(self):
        super(CheckBox, self).__init__()
        self.hotspot = None
        self.onKeyEventObserver = None
        pass

    def _onInitialize(self, obj):
        super(CheckBox, self)._onInitialize(obj)
        self.hotspot = self.createChild("HotSpotPolygon")
        self.hotspot.setEventListener(onHandleMouseButtonEvent=self._onMouseButtonEvent)
        self.hotspot.enable()

        if self.KeyTag is not None:
            self.KeyHandlerID = Menge.addKeyHandler(self.__onKeyEvent)
            pass
        pass

    def _onFinalize(self):
        super(CheckBox, self)._onFinalize()

        Menge.destroyNode(self.hotspot)
        self.hotspot = None

        if self.KeyTag is not None:
            Menge.removeGlobalHandler(self.KeyHandlerID)
            pass
        pass

    def __onKeyEvent(self, event):
        if event.isDown != True:
            return False
            pass

        KeyTag = CheckBox.s_keys[self.KeyTag]
        if KeyTag == event.code:
            self._mouseClick()
            pass

        return False
        pass

    def _restorePolygon(self, value):
        self.hotspot.setPolygon(value)
        pass

    def _updateState(self, value):
        if self.BlockState is True:
            return False

        Sprite_Check = self.object.getObject("Sprite_Check")
        Sprite_Check.setEnable(value)

        if self.object.hasObject("Sprite_Uncheck"):
            Sprite_Uncheck = self.object.getObject("Sprite_Uncheck")
            Sprite_Uncheck.setEnable(not value)
            pass
        pass

    def _onActivate(self):
        super(CheckBox, self)._onActivate()
        pass

    def _onMouseButtonEvent(self, touchId, x, y, button, pressure, isDown, isPressed):
        if button != 0:
            return False
            pass

        if isDown is True:
            self._mouseClick()
            pass

        return True
        pass

    def _mouseClick(self):
        if self.BlockState is True:
            return False
            pass

        state = self.object.getParam("State")
        new_state = not state
        self.object.setParam("State", new_state)

        Notification.notify(Notificator.onCheckBox, self.object, new_state)
        pass
    pass