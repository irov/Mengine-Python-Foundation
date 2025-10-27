Interaction = Mengine.importEntity("Interaction")

class Button(Interaction):
    s_keys = dict(Esc=Mengine.KC_ESCAPE, Enter=Mengine.KC_RETURN)

    @staticmethod
    def declareORM(Type):
        Interaction.declareORM(Type)

        Type.addAction("TextID", Update=Button._updateTextID)
        Type.addAction("TextArgs", Update=Button._updateTextArgs)
        Type.addAction("TextPosition", Update=Button.__updateTextPosition)
        Type.addAction("TextPositionDown")
        Type.addAction("TextPositionOver")
        Type.addAction("TextAlign", Update=Button.__updateAlign)
        Type.addAction("TextVerticalAlign", Update=Button.__updateVerticalAlign)
        Type.addAction("TextLineOffset", Update=Button.__updateLineOffset)

        Type.addAction("Font", Update=Button._updateFont)
        Type.addAction("FontRGBA", Update=Button.__updateFontRGBA)

        Type.addAction("BlockState")
        Type.addAction("BlockKeys")
        Type.addAction("onUp")
        Type.addAction("onDown")
        Type.addAction("onOver")
        Type.addAction("KeyTag")
        Type.addAction("SoundTag")
        Type.addAction("SoundTagEnter")
        pass

    def __init__(self):
        super(Button, self).__init__()

        self.text = None
        self.currentState = "onUp"

        self.__wasClicked = False

        self.states = {}
        pass

    def _onInitialize(self, obj):
        super(Button, self)._onInitialize(obj)

        # i think order is important
        buttons = [self.onUp, self.onOver, self.onDown]

        for button in buttons:
            Name = button["Name"]
            ResourceName = button["Resource"]
            Resource = Mengine.getResourceReference(ResourceName)
            sprite = Mengine.createSprite(Name, Resource)

            Position = button["Position"]
            sprite.setLocalPosition(Position)

            self.addChild(sprite)

            self.states[Name] = sprite
            pass

        self.text = self.createChild("TextField")

        name = self.getName()
        self.text.setName(name)

        self.text.disable()
        pass

    def _onFinalize(self):
        super(Button, self)._onFinalize()

        Mengine.destroyNode(self.text)
        self.text = None

        for state in self.states.itervalues():
            Mengine.destroyNode(state)
            pass

        self.states = {}

        # self.enableGlobalMouseEvent(False)
        # self.setEventListener(onGlobalHandleMouseButtonEvent = None)
        pass

    def _keyEvent(self, event):
        if self.KeyTag is None:
            return self.BlockKey

        if Mengine.isExclusiveKeyDown(event.code) is False:
            return self.BlockKey

        if isDown is False:
            return self.BlockKey

        if self.BlockState is True:
            return self.BlockKey

        if self.BlockKeys is True:
            return self.BlockKey

        if self.object.getEnable() is False:
            return self.BlockKey

        KeyTag = Button.s_keys[self.KeyTag]
        if KeyTag == key:
            Notification.notify(Notificator.onButtonClick, self.object)
            pass

        return self.BlockKey

    def resetSpritesPosition(self):
        sprites = self.getSprites()
        for sprite in sprites:
            sprite.setLocalPosition((0, 0))
            pass
        pass

    def getSprites(self):
        sprites = []
        buttons = [self.onUp, self.onOver, self.onDown]

        for button in buttons:
            buttonName = button["Name"]
            sprite = self.states[buttonName]
            sprites.append(sprite)
            pass

        return sprites
        pass

    def _restoreTextID(self, value):
        if value is None:
            self.text.removeTextId()
            return
            pass

        self.text.setTextId(value)
        pass

    def _updateTextID(self, value):
        if value is None:
            self.text.removeTextId()
            return
            pass

        if self.TextPosition is None:
            Trace.log("Entity", 0, "Button '%s' in group '%s' hasn't 'TextPosition' but have 'TextID' == '%s'!!!!!" % (self.getName(), self.object.getGroupName(), value))
            return
            pass

        self.text.setTextId(value)
        pass

    def _updateTextArgs(self, args):
        if args is None:
            self.text.removeTextFormatArgs()
            return
            pass

        if isinstance(args, tuple) is True:
            self.text.setTextFormatArgs(*args)
        else:
            self.text.setTextFormatArgs(args)
            pass
        pass

    def _updateFont(self, value):
        if value is None:
            return
            pass

        self.text.setFontName(value)
        pass

    def __updateTextPosition(self, position):
        if position is None:
            return
            pass

        self.text.setLocalPosition(position)
        pass

    def _onPreparation(self):
        super(Button, self)._onPreparation()

        self.setState(self.currentState)
        pass

    def _onActivate(self):
        super(Button, self)._onActivate()

        self.text.enable()

        self.MouseButtonHandlerID = Mengine.addMouseButtonHandler(self.__onGlobalHandleMouseButtonEvent)
        pass

    def _onDeactivate(self):
        super(Button, self)._onDeactivate()

        Mengine.removeGlobalHandler(self.MouseButtonHandlerID)
        self.MouseButtonHandlerID = None
        pass

    def _mouseClickBegin(self, x, y):
        if self.BlockState is True:
            return
            pass

        Notification.notify(Notificator.onButtonClickBegin, self.object)
        pass

    def _mouseClick(self, x, y):
        if self.BlockState is True:
            return
            pass

        Notification.notify(Notificator.onButtonSoundClick, self.SoundTag)
        Notification.notify(Notificator.onButtonClick, self.object)
        pass

    def _mouseClickEnd(self, x, y):
        self.__wasClicked = True
        self.setState("onDown")
        pass

    def _mouseClickEndUp(self, x, y):
        if self.isState("onDown") is True or self.wasClicked():
            Notification.notify(Notificator.onButtonClickEndUp, self.object)
            self.setState("onUp")
            pass
        pass

    def __onGlobalHandleMouseButtonEvent(self, event):
        if event.isDown is True:
            self.__wasClicked = False
            pass
        pass

    def _mouseLeave(self):
        if self.BlockState is True:
            return

        self.setState("onUp")

        Notification.notify(Notificator.onButtonMouseLeave, self.object)
        pass

    def _mouseEnter(self, x, y):
        if self.BlockState is True:
            return

        self.setState("onOver")

        Notification.notify(Notificator.onButtonSoundEnter, self.SoundTagEnter)
        Notification.notify(Notificator.onButtonMouseEnter, self.object)
        pass

    def setState(self, state):
        if self.BlockState is True:
            return
            pass

        sprite = self.states[state]

        if sprite is None:
            Trace.log("Entity", 0, "Button '%s' not found state '%s'" % (self.getName(), state))
            return
            pass

        for image in self.states.itervalues():
            image.disable()
            pass

        sprite.enable()
        self.currentState = state

        self._updateTextPosition()
        pass

    def isState(self, state):
        return self.currentState == state
        pass

    def getState(self):
        return self.currentState
        pass

    def getSprite(self):
        sprite = self.states[self.currentState]
        return sprite
        pass

    def wasClicked(self):
        return self.__wasClicked
        pass

    def __updateFontRGBA(self, rgba):
        if rgba is None:
            return
            pass

        self.text.setFontColor(rgba)
        pass

    def _updateTextPosition(self):
        if self.TextPosition and self.isState("onUp"):
            self.text.setLocalPosition(self.TextPosition)
            pass
        elif self.TextPositionDown and self.isState("onDown"):
            self.text.setLocalPosition(self.TextPositionDown)
            pass
        elif self.TextPositionOver and self.isState("onOver"):
            self.text.setLocalPosition(self.TextPositionOver)
            pass
        pass

    def __updateAlign(self, align):
        if align == "Center":
            self.text.setHorizontalCenterAlign()
            pass
        elif align == "Right":
            self.text.setHorizontalRightAlign()
            pass
        elif align == "Left":
            self.text.setHorizontalLeftAlign()
            pass
        else:
            Trace.log("Entity", 0, "Button.__updateAlign invalid align mode '%s'" % (align))
            pass
        pass

    def __updateVerticalAlign(self, align):
        if align == "Bottom":
            self.text.setVerticalBottomAlign()
            pass
        elif align == "Center":
            self.text.setVerticalCenterAlign()
            pass
        elif align == "Top":
            self.text.setVerticalTopAlign()
            pass
        else:
            Trace.log("Entity", 0, "Button.__updateVerticalAlign invalid align mode '%s'" % (align))
            pass
        pass

    def __updateLineOffset(self, offset):
        if offset is None:
            return
            pass

        self.text.setLineOffset(offset)
        pass

    pass