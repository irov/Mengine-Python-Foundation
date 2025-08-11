from Foundation.Entity.BaseEntity import BaseEntity
from Foundation.TaskManager import TaskManager


class EditBox(BaseEntity):
    @staticmethod
    def declareORM(Type):
        BaseEntity.declareORM(Type)

        Type.addAction(Type, "Polygon", Update=EditBox.__restorePolygon)
        Type.addAction(Type, "Wrap", Update=EditBox.__restoreWrap)

        Type.addAction(Type, "Value", Update=EditBox.updateValue)
        Type.addAction(Type, "Focus", Update=EditBox._updateFocus)
        Type.addAction(Type, "PasswordChar", Update=EditBox._updatePasswordChar)
        Type.addAction(Type, "BlackList")
        Type.addAction(Type, "TextLengthLimit")

    def __init__(self):
        super(EditBox, self).__init__()

        self.maxLength = 0.0
        self.hotspot = None

        self.valueByDefault = None

        self.Sprite_Carriage = None

        self.text = u""
        self.carriage = 0
        self.prev_carriage = 0  # for blinking on (when staying) or off (when moving)

        self.tc_blink_carriage = None

        self.isActive = True

    def _onInitialize(self, obj):
        super(EditBox, self)._onInitialize(obj)

        self.hotspot = self.createChild("HotSpotPolygon")
        self.hotspot.setEventListener(onHandleMouseButtonEvent=self._onMouseButtonEvent)
        self.hotspot.enable()
        pass

    def _onFinalize(self):
        super(EditBox, self)._onFinalize()

        Mengine.destroyNode(self.hotspot)
        self.hotspot = None

        self.Sprite_Carriage = None
        pass

    def __restorePolygon(self, Polygon):
        if Polygon is None:
            return
            pass

        self.hotspot.setPolygon(Polygon)
        pass

    def __restoreWrap(self, value):
        self.maxLength = value[1][0] - value[0][0]
        pass

    def _updateFocus(self, value):
        if self.isActivate() is False:
            return

        # this must be tested on current HOPA projects
        self.Sprite_Carriage.setEnable(value)

    def _updatePasswordChar(self, value):
        text = self.object.getParam("Value")
        self.object.setParam("Value", text)
        pass

    def setText(self, TextObject, TextValue):
        if TextObject is None:
            return

        # if password char not None than replace all text by its value
        password_char = self.object.getParam("PasswordChar")
        if password_char is not None:
            TextValue = password_char * len(TextValue)
            pass

        TextObject.setTextArgs(TextValue)
        pass

    def updateValue(self, value):
        self.text = value

        Text_Value = self.object.getObject("Text_Value")
        Text_Value.setEnable(True)

        # Text_Value.setTextArgs(value)
        self.setText(Text_Value, value)

        self.Sprite_Carriage = self.object.getObject("Sprite_Carriage")

        posX = Text_Value.getPosition()
        posY = self.Sprite_Carriage.getPosition()
        self.pos = (round(posX[0]), round(posY[1]))

        # self.carriage = len(self.text)

        if self.node.isActivate() is True:
            self.updateCarriage()
            pass

        if len(value) is 0:
            Notification.notify(Notificator.EditBoxEmpty, self.object)
            pass
        else:
            Notification.notify(Notificator.EditBoxChange, self.object)

    def _onPreparation(self):
        super(EditBox, self)._onPreparation()
        self._SceneRestartBeginID = Notification.addObserver(Notificator.onSceneRestartBegin, self._onSceneRestartBegin)
        pass

    def _onActivate(self):
        super(EditBox, self)._onActivate()

        self.KeyHandlerID = Mengine.addKeyHandler(self.__onGlobalHandleKeyEvent)
        self.TextHandlerID = Mengine.addTextHandler(self.__onGlobalHandleTextEvent)

        self.updateCarriage()

        self.setActive(True)
        pass

    def _onDeactivate(self):
        super(EditBox, self)._onDeactivate()
        self.setActive(False)
        self.Sprite_Carriage.setPosition(self.pos)
        self.text = u""

        if self._SceneRestartBeginID is not None:
            Notification.removeObserver(self._SceneRestartBeginID)
            self._SceneRestartBeginID = None

        if self.KeyHandlerID is not None:
            Mengine.removeGlobalHandler(self.KeyHandlerID)
            self.KeyHandlerID = None
        if self.TextHandlerID is not None:
            Mengine.removeGlobalHandler(self.TextHandlerID)
            self.TextHandlerID = None

    def setValueByDefault(self, value):
        self.valueByDefault = value
        pass

    def _onMouseButtonEvent(self, context, event):
        if event.isDown is False:
            Notification.notify(Notificator.EditBoxUnhold, self.object)
            return True

        if self.valueByDefault is not None:
            self.object.setParam("Value", u"")
            self.valueByDefault = None
            self.carriage = 0

        self.mouseXToCarriage(event.position.world.x)

        self.updateCarriage()

        self.showKeyboard(True)

        Notification.notify(Notificator.EditBoxFocus, self.object)

        return True

    def _onSceneRestartBegin(self):
        self.showKeyboard(False)
        return False

    def __onGlobalHandleKeyEvent(self, event):
        if event.isDown is False:
            return
            pass

        if self.object.getFocus() is False:
            return
            pass

        if event.isRepeat is False:
            Notification.notify(Notificator.EditBoxKeyEvent, self.object, event.code)
            pass

        if event.code == Mengine.KC_LEFT:
            self.carriageShift(-1)
        elif event.code == Mengine.KC_RIGHT:
            self.carriageShift(1)
        elif event.code == Mengine.KC_DELETE:
            self.deleteSymbol()
        elif event.code == Mengine.KC_HOME:
            self.carriageHome()
        elif event.code == Mengine.KC_END:
            self.carriageEnd()
        elif event.code == Mengine.KC_BACK:
            self.backspaceSymbol()
            pass
        pass

    def __onGlobalHandleTextEvent(self, event):
        if self.object.getFocus() is False:
            return
            pass

        if ord(event.symbol) > 0x1f and ord(event.symbol) != 0x7f and not (0x80 <= ord(event.symbol) <= 0x9f):
            self.addSymbol(event.symbol)
            pass
        pass

    def carriageShift(self, shift):
        self.carriage += shift
        if self.carriage < 0:
            self.carriage = 0
            pass

        if self.carriage > len(self.text):
            self.carriage = len(self.text)
            pass

        self.updateCarriage()
        pass

    def carriageHome(self):
        self.carriage = 0
        self.updateCarriage()
        pass

    def carriageEnd(self):
        self.carriage = len(self.text)
        self.updateCarriage()
        pass

    def addSymbol(self, symbol):
        if self.isActive is False:
            return

        if symbol == " " and len(self.text) == 0:
            return

        if symbol in self.BlackList:
            return

        text = self.text[:self.carriage] + symbol + self.text[self.carriage:]

        if self.TextLengthLimit is not None and self.TextLengthLimit < len(text):
            return

        Text_Value = self.object.getObject("Text_Value")
        # Text_Value.setTextArgs((text,))
        self.setText(Text_Value, text)

        textEditBox = Text_Value.getEntity()
        length = textEditBox.getLength()

        if length.x <= self.maxLength:
            self.text = text
            self.carriage += 1

        self.object.setParam("Value", self.text)
        pass

    def deleteSymbol(self):
        if self.isActive is False:
            return

        if self.carriage == len(self.text):
            return

        self.text = self.text[:self.carriage] + self.text[self.carriage + 1:]

        self.object.setParam("Value", self.text)
        pass

    def backspaceSymbol(self):
        if self.isActive is False:
            return

        if self.carriage == 0:
            return
            pass

        newCarriage = self.carriage - 1
        self.text = self.text[:newCarriage] + self.text[self.carriage:]

        self.carriage = newCarriage

        self.object.setParam("Value", self.text)
        pass

    def updateCarriage(self):
        bufText = self.text[:self.carriage]

        Text_Value = self.object.getObject("Text_Value")

        textEditBox = Text_Value.getEntity()
        full_length = textEditBox.getLength()

        # Text_Value.setTextArgs((bufText,))
        self.setText(Text_Value, bufText)

        bufTextLength = textEditBox.getLength()
        carriage_offset_from_left_border = bufTextLength.x

        left_text_value_border_pos_x = self.pos[0] - (full_length.x * 0.5)

        carriage_pos_y = self.pos[1]
        carriage_pos = (left_text_value_border_pos_x + carriage_offset_from_left_border, carriage_pos_y)

        self.Sprite_Carriage.setPosition(carriage_pos)

        # Text_Value.setTextArgs((self.text,))
        self.setText(Text_Value, self.text)
        pass

    def _runTaskChains(self):
        # blink carriage
        self.tc_blink_carriage = TaskManager.createTaskChain(Name="%s_TC" % self.getName(), Repeat=True)
        with self.tc_blink_carriage as tc:
            tc.addDelay(500.0)
            tc.addFunction(self.blinkCarriage)

    def showKeyboard(self, state):
        if Mengine.hasTouchpad() is False:
            return

        if state is True and Mengine.isShowKeyboard() is False:
            Mengine.showKeyboard()
            Notification.notify(Notificator.onMobileKeyboardShow, True)
        elif state is False and Mengine.isShowKeyboard() is True:
            Mengine.hideKeyboard()
            Notification.notify(Notificator.onMobileKeyboardShow, False)

    def blinkCarriage(self):
        sprite_enable = self.Sprite_Carriage.getEnable()
        if self.prev_carriage == self.carriage:
            self.Sprite_Carriage.setEnable(not sprite_enable)
        elif not sprite_enable:
            self.Sprite_Carriage.setEnable(True)
        self.prev_carriage = self.carriage
        pass

    def mouseXToCarriage(self, mouse_x):
        Text_Value = self.object.getObject("Text_Value")
        textEditBox = Text_Value.getEntity()
        full_length = textEditBox.getLength()

        left_text_value_border_pos_x = self.pos[0] - (full_length.x * 0.5)
        distance_to_text_start_by_x = left_text_value_border_pos_x - mouse_x

        text_len = len(self.text)

        if full_length.x != 0:
            text_len_percent = -distance_to_text_start_by_x / full_length.x
            float_pos = text_len_percent * text_len
            self.carriage = int(round(float_pos))
        else:
            self.carriage = 0

        if self.carriage < 0:
            self.carriage = 0

        if self.carriage > text_len:
            self.carriage = len(self.text)

    def setActive(self, state):
        self.isActive = state

        Text_Value = self.object.getObject("Text_Value")
        if state is True:
            if self.tc_blink_carriage is None:
                self._runTaskChains()
            Text_Value.setAlpha(1.0)
            self.hotspot.enable()
            self.showKeyboard(True)
        else:
            Text_Value.setAlpha(0.0)
            if self.tc_blink_carriage is not None:
                self.tc_blink_carriage.cancel()
                self.tc_blink_carriage = None
            self.hotspot.disable()
            self.showKeyboard(False)

        self.Sprite_Carriage.setEnable(state)

        Notification.notify(Notificator.onEditboxSetActive, self.object.getName(), state)

    def setTextLengthLimit(self, length):
        if length < 0:
            Trace.log("Entity", 0, "EditBox.setTextLengthLimit: length must be >= 0 (your input = {})".format(length))
            return

        self.object.setParam("TextLengthLimit", length)