from Foundation.Entity.BaseEntity import BaseEntity
from Foundation.ObjectManager import ObjectManager
from Foundation.TaskManager import TaskManager
from Notification import Notification

class MovieEditBox(BaseEntity):
    # __metaclass__ = finalslots("tc", "state", "Movies", "SemaphoreBlock", "max")

    @staticmethod
    def declareORM(Type):
        BaseEntity.declareORM(Type)

        # MovieButton part
        Type.addActionActivate(Type, "ResourceMovieIdle")
        Type.addActionActivate(Type, "ResourceMovieOver")
        Type.addActionActivate(Type, "ResourceMovieFocus")
        Type.addActionActivate(Type, "ResourceMovieCarriage", Update=Type.__updateCarriage)
        Type.addActionActivate(Type, "ResourceMovieSlider")
        Type.addActionActivate(Type, "ResourceMovieBlock")

        # EditBox
        Type.addActionActivate(Type, "Text_ID")
        Type.addActionActivate(Type, "Text_Present_ID")
        Type.addActionActivate(Type, "Value", Update=Type._updateValue)
        Type.addActionActivate(Type, "Focus", Update=Type._updateFocus)
        Type.addActionActivate(Type, "PasswordChar", Update=Type._updatePasswordChar)
        Type.addActionActivate(Type, "BlackList")
        Type.addActionActivate(Type, "Block", Update=Type.__updateBlock)
        Type.addActionActivate(Type, "Present", Update=Type.__updatePresent)
        pass

    def __updateCarriage(self, value):
        StartNode = self.Movies.get("Carriage").getEntity().getMovieSlot("start")
        EndNode = self.Movies.get("Carriage").getEntity().getMovieSlot("end")
        CarriageMinX = StartNode.getWorldPosition().x
        CarriageMaxX = EndNode.getWorldPosition().x
        self.maxLength = CarriageMaxX - CarriageMinX

        pass

    def __updatePresent(self, value):
        if self.state is not 'Focus' and len(self.object.getValue()) == 0:
            self.setText(self.__getText(), value)
        pass

    def __updateBlock(self, value):
        if value == True:
            self.SemaphoreBlock.setValue(True)
            return
            pass

        self.SemaphoreBlock.setValue(False)
        pass

    def _updateFocus(self, value):
        if self.isActivate() is False:
            return
        self.Movies.get("Carriage").setEnable(value)
        if value is False:
            self.__activate_slider(False)
        self.SemaphoreFocus.setValue(value)
        pass

    def __activate_slider(self, value):
        if Menge.hasTouchpad() is False:
            return

        MovieSlider = self.Movies.get("Slider")
        MovieSlider.setEnable(value)
        if self.tc_slider is not None:
            self.tc_slider.cancel()
            self.tc_slider = None
            pass
        if value is True:
            self.tc_slider = TaskManager.createTaskChain(Repeat=True)
            with self.tc_slider as tc:
                with tc.addRaceTask(2) as (tc_on_down, tc_on_up):
                    tc_on_down.addTask("TaskMovieSocketClick", SocketName="socket", Movie=MovieSlider, isDown=True)
                    tc_on_down.addFunction(self.__on_slide, True)
                    tc_on_down.addFunction(Menge.enableGlobalHandler, self._mouse_move_handler, True)

                    tc_on_up.addTask("TaskMouseButtonClick", isDown=False)
                    tc_on_up.addFunction(self.__on_slide, False)
                    tc_on_up.addFunction(Menge.enableGlobalHandler, self._mouse_move_handler, False)
                    pass

    def _updatePasswordChar(self, value):
        text = self.object.getParam("Value")
        self.object.setParam("Value", text)
        pass

    def set_present_text(self, old_value):
        text_field = self.__getPresentText()
        present_text = self.object.getPresent()

        if text_field is not None:
            if len(old_value) == 0 and self.state is not 'Focus':
                text_field.setTextFormatArgs(present_text)
                return u''
            else:
                text_field.setTextFormatArgs('')
                return old_value
        else:
            if len(old_value) == 0 and self.state is not 'Focus':
                return present_text
            else:
                return old_value
        pass

    def setText(self, TextObject, TextValue):
        if TextObject is None:
            return

        # if password char not None than replace all text by its value
        password_char = self.object.getParam("PasswordChar")
        if password_char is not None:
            TextValue = password_char * len(TextValue)
            pass

        TextValue = self.set_present_text(TextValue)

        TextObject.setTextFormatArgs(TextValue)
        pass

    def __move_text(self, text_field):
        new_pos = (self.startPos[0] - self.text_move_distance, self.startPos[1])
        text_field.setWorldPosition(new_pos)
        pass

    def __getText(self):
        movie = self.Movies.get(self.state)
        if movie is None:
            movie = self.Movies.get("Idle")
        if movie.getEntity().hasMovieText(self.object.getText_ID()) is False:
            return None

        textField = movie.getEntity().getMovieText(self.object.getText_ID())
        return textField
        pass

    def __getPresentText(self):
        movie = self.Movies.get(self.state)
        if movie is None:
            movie = self.Movies.get("Idle")
        movie = movie.getEntity()
        if movie.hasMovieText(self.object.getText_Present_ID()) is False:
            return None

        textField = movie.getMovieText(self.object.getText_Present_ID())
        return textField
        pass

    def updateValue(self):
        text = self.object.getParam("Value")
        self.object.setParam("Value", text)

    def _updateValue(self, value):
        self.text = value

        Text_Value = self.__getText()
        self.setText(Text_Value, value)

        if self.node.isActivate() is True and self.object.getFocus() is True:
            self.updateCarriage()
            pass

        if len(value) is 0:
            Notification.notify(Notificator.MovieEditBoxEmpty, self.object)
            pass
        else:
            Notification.notify(Notificator.MovieEditBoxChange, self.object)
            pass
        pass

    def __init__(self):
        super(MovieEditBox, self).__init__()
        # EditBox part

        self.maxLength = 0.0

        self.text = u""
        self.carriage = 0

        self.text_move_distance = 0

        self.lockSlider = False
        self.sliderEndPos = 0
        self.tc_slider = None

        self.vocabluary = {}

        # MovieButton part
        self.tc = None
        self.state = "Idle"

        self.Movies = {}

        self.SemaphoreBlock = Semaphore(False, "MovieEditBoxBlock")
        self.SemaphoreFocus = Semaphore(False, "MovieEditBoxFocus")

        pass

    def __add_to_vocabluary(self, text_field, char):
        self.setText(text_field, char)
        self.vocabluary[char] = text_field.getTextSize().x
        pass

    def _onInitialize(self, obj):
        super(MovieEditBox, self)._onInitialize(obj)

        def __createMovie(name, res, play, loop):
            if res is None:
                return None
                pass

            if Menge.hasResource(res) is False:
                return False
                pass

            resource = Menge.getResourceReference(res)

            if resource is None:
                Trace.log("Entity", 0, "MovieEditBox._onInitialize: not fount resource %s" % (res))
                return None
                pass

            mov = ObjectManager.createObjectUnique("Movie", name, self.object, ResourceMovie=resource)
            mov.setEnable(False)
            mov.setPlay(play)
            mov.setLoop(loop)

            movEntityNode = mov.getEntityNode()
            self.addChild(movEntityNode)

            self.Movies[name] = mov

            return mov
            pass

        __createMovie("Idle", self.ResourceMovieIdle, True, False)
        __createMovie("Over", self.ResourceMovieOver, True, False)
        __createMovie("Focus", self.ResourceMovieFocus, True, False)
        __createMovie("Block", self.ResourceMovieBlock, True, False)

        __createMovie("Carriage", self.ResourceMovieCarriage, True, True)
        __createMovie("Slider", self.ResourceMovieSlider, True, False)

        focus_movie = self.Movies.get("Focus", None)
        if focus_movie is None:
            focus_movie = self.Movies.get('Idle')

        focus_movie.getEntity().getSocket("socket").setEventListener(onHandleMouseButtonEvent=self._onMouseButtonEventFocus)

        self._mouse_move_handler = Menge.addMouseMoveHandler(self.on_mouse_move)
        Menge.enableGlobalHandler(self._mouse_move_handler, False)

        # set vocabluary

        text_field = self.__getText()
        self.startPos = text_field.getWorldPosition()
        for i in range(26):
            self.__add_to_vocabluary(text_field, chr(ord('a') + i))
            self.__add_to_vocabluary(text_field, chr(ord('A') + i))
        self.__add_to_vocabluary(text_field, ' ')

        return True
        pass

    def _onMouseButtonEventFocus(self, touchId, x, y, button, pressure, isDown, isPressed):
        if isDown is False:
            return True
        self.__activate_slider(True)
        cursor_pos = x - self.startPos[0]
        self.carriage = self.__get_new_carriage_pos(cursor_pos)
        self.updateCarriage()
        return True
        pass

    def __setState(self, state):
        self.state = state
        pass

    def __stateIdle(self, source, MovieIdle):
        source.addEnable(MovieIdle)
        source.addDelay(0.0)
        source.addFunction(self.updateValue)
        with source.addRaceTask(4) as (source_over_click, source_over_enter, source_block, source_tab_focus):
            source_over_click.addTask("TaskMovieSocketClick", SocketName="socket", Movie=MovieIdle, isDown=True)
            source_over_click.addFunction(self.__setState, "Focus")

            source_over_enter.addTask("TaskMovieSocketEnter", SocketName="socket", Movie=MovieIdle)
            source_over_enter.addFunction(self.__setState, "Over")

            source_block.addSemaphore(self.SemaphoreBlock, From=True)
            source_block.addFunction(self.__setState, "Block")

            source_tab_focus.addSemaphore(self.SemaphoreFocus, From=True)
            source_tab_focus.addFunction(self.__setState, "Focus")
            pass

        source.addDisable(MovieIdle)
        pass

    def __stateOver(self, source, MovieOver):
        if MovieOver is None:
            source.addFunction(self.__setState, "Focus")
            return
            pass

        source.addEnable(MovieOver)
        source.addDelay(0.0)
        source.addFunction(self.updateValue)
        # cDict = dict(
        #     dimension1='Hangar',
        #     metric2=228
        # )
        # source.addTask('TaskSendAnalytics', clientID='555', category='Over', action='Enter', client_definition=cDict)
        # source.addFacebookAuth(response_type='code', scope='publish_actions,public_profile')
        with source.addRaceTask(4) as (source_over_click, source_over_leave, source_block, source_tab_focus):
            source_over_click.addTask("TaskMovieSocketClick", SocketName="socket", Movie=MovieOver, isDown=True, Already=True)
            source_over_click.addFunction(self.__setState, "Focus")

            source_over_leave.addTask("TaskMovieSocketLeave", SocketName="socket", Movie=MovieOver)
            source_over_leave.addFunction(self.__setState, "Idle")

            source_block.addSemaphore(self.SemaphoreBlock, From=True)
            source_block.addFunction(self.__setState, "Block")

            source_tab_focus.addSemaphore(self.SemaphoreFocus, From=True)
            source_tab_focus.addFunction(self.__setState, "Focus")
            pass

        source.addDisable(MovieOver)
        pass

    def __stateFocus(self, source, MovieFocus):
        if MovieFocus is None:
            source.addTask("TaskNotify", ID=Notificator.onMovieEditBoxFocus, Args=(self.object,))
            source.addEnable(self.Movies.get("Idle"))
            source.addSemaphore(self.SemaphoreFocus, From=False)
            source.addFunction(self.__setState, "Idle")
            source.addDisable(self.Movies.get("Idle"))
            return
            pass

        def cb(data):
            pass

        source.addEnable(MovieFocus)

        source.addTask("TaskNotify", ID=Notificator.onMovieEditBoxFocus, Args=(self.object,))
        source.addFunction(self.updateValue)
        # source.addFacebookMessage(message='HelloAgainAndAgain2456')
        # source.addFacebookData(cb = cb, fields = 'id,name,last_name')
        source.addSemaphore(self.SemaphoreFocus, From=False)
        source.addFunction(self.__setState, "Idle")

        source.addDisable(MovieFocus)
        pass

    def __stateBlock(self, source, MovieBlock):
        if MovieBlock is None:
            source.addEnable(self.Movies.get("Idle"))
            source.addSemaphore(self.SemaphoreBlock, From=False)
            source.addFunction(self.__setState, "Idle")
            source.addDisable(self.Movies.get("Idle"))
            return
            pass

        source.addEnable(MovieBlock)
        source.addFunction(self.updateValue)

        source.addSemaphore(self.SemaphoreBlock, From=False)
        source.addFunction(self.__setState, "Idle")

        source.addDisable(MovieBlock)
        pass

    def _onActivate(self):
        super(MovieEditBox, self)._onActivate()

        self.KeyHandlerID = Menge.addKeyHandler(self.__onGlobalHandleKeyEvent)
        self.TextHandlerID = Menge.addTextHandler(self.__onGlobalHandleTextEvent)

        # self.updateCarriage()

        Menge.showKeyboard()

        # MovieButton part
        MovieIdle = self.Movies.get("Idle")
        MovieOver = self.Movies.get("Over", MovieIdle)
        MovieFocus = self.Movies.get("Focus")
        MovieBlock = self.Movies.get("Block")
        self.state = "Idle"

        self.tc = TaskManager.createTaskChain(Repeat=True, NoCheckAntiStackCycle=True)

        with self.tc as source_repeat:
            Scopes = dict(Idle=Functor(self.__stateIdle, MovieIdle), Over=Functor(self.__stateOver, MovieOver), Focus=Functor(self.__stateFocus, MovieFocus), Block=Functor(self.__stateBlock, MovieBlock), )

            def __states(isSkip, cb):
                cb(isSkip, self.state)
                pass

            source_repeat.addScopeSwitch(Scopes, __states)
            pass

        def cb(one, two, three, four, params):
            pass

        pass

    def __moveText(self, text_field):
        text_field.setWorldPosition((text_field.getWorldPosition().x + 50, text_field.getWorldPosition().y))
        pass

    def __on_slide(self, value):
        if self.lockSlider is False and value is False:
            return
        self.lockSlider = value
        if value is False:
            self.carriage = self.__get_new_carriage_pos(self.sliderEndPos)
            self.updateCarriage()
        pass

    def _onDeactivate(self):
        super(MovieEditBox, self)._onDeactivate()
        self.text = u""

        Menge.removeGlobalHandler(self.KeyHandlerID)
        Menge.removeGlobalHandler(self.TextHandlerID)

        Menge.hideKeyboard()

        if self.tc is not None:
            self.tc.cancel()
            self.tc = None
            pass

        if self.tc_slider is not None:
            self.tc_slider.cancel()
            self.tc_slider = None
            pass

        for mov in self.Movies.itervalues():
            mov.setEnable(False)
            pass

        pass

    def _onFinalize(self):
        super(MovieEditBox, self)._onFinalize()

        for mov in self.Movies.itervalues():
            mov.onDestroy()
            pass

        self.Movies = {}
        pass

    # EDITING EVENTS

    def __onGlobalHandleKeyEvent(self, event):
        if event.isDown is False:
            return
            pass

        if self.object.getFocus() is False:
            return
            pass

        if event.isRepeat is False:
            Notification.notify(Notificator.MovieEditBoxKeyEvent, self.object, event.code)
            pass

        self.__activate_slider(False)

        if event.code == Menge.KC_LEFT:
            self.carriageShift(-1)
        elif event.code == Menge.KC_RIGHT:
            self.carriageShift(1)
        elif event.code == Menge.KC_DELETE:
            self.deleteSymbol()
        elif event.code == Menge.KC_HOME:
            self.carriageHome()
        elif event.code == Menge.KC_END:
            self.carriageEnd()
        elif event.code == Menge.KC_BACK:
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
        if symbol == " " and len(self.text) == 0:
            return
            pass

        if symbol in self.BlackList:
            return
            pass

        if symbol not in self.vocabluary:
            self.__add_to_vocabluary(self.__getText(), symbol)

        text = self.text[:self.carriage] + symbol + self.text[self.carriage:]

        self.text = text
        self.carriage += 1

        self.object.setParam("Value", self.text)
        pass

    def deleteSymbol(self):
        if self.carriage == len(self.text):
            return

        self.text = self.text[:self.carriage] + self.text[self.carriage + 1:]
        self.object.setParam("Value", self.text)
        pass

    def backspaceSymbol(self):
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

        # move text field according to carriage pos if carriage out of view port -> move text field
        carriage_offset_from_left_border = self.get_text_width(bufText)
        if carriage_offset_from_left_border > self.maxLength + self.text_move_distance:
            self.text_move_distance = carriage_offset_from_left_border - self.maxLength
            pass
        elif carriage_offset_from_left_border < self.text_move_distance:
            self.text_move_distance = carriage_offset_from_left_border
        carriage_offset_from_left_border -= self.text_move_distance

        carriage_pos = (carriage_offset_from_left_border, self.Movies.get("Carriage").getEntityNode().getWorldPosition()[1])

        self.Movies.get("Carriage").getEntityNode().setWorldPosition(carriage_pos)
        if self.lockSlider is False:
            self.Movies.get("Slider").getEntityNode().setWorldPosition(carriage_pos)

        # Text_Value.setTextArgs((self.text,))
        self.__move_text(self.__getText())
        pass

    def __get_new_carriage_pos(self, pos):
        pos += self.text_move_distance
        new_carriage = 1
        while self.get_text_width(self.text[:new_carriage]) < pos and new_carriage <= len(self.text):
            new_carriage += 1
            pass
        if new_carriage == len(self.text) + 1:
            return new_carriage
        return new_carriage - 1

    def on_mouse_move(self, event):
        new_slider_pos = (event.x - self.startPos[0], self.Movies.get("Slider").getEntityNode().getWorldPosition().y)
        self.Movies.get("Slider").getEntityNode().setWorldPosition(new_slider_pos)
        if new_slider_pos[0] < 0:
            self.Movies.get("Carriage").getEntityNode().setWorldPosition((0, new_slider_pos[1]))
        elif new_slider_pos[0] > self.maxLength:
            self.Movies.get("Carriage").getEntityNode().setWorldPosition((self.maxLength, new_slider_pos[1]))
        else:
            self.Movies.get("Carriage").getEntityNode().setWorldPosition(new_slider_pos)
        self.sliderEndPos = new_slider_pos[0]
        pass

    def get_text_width(self, text_value):
        length = 0
        for char in text_value:
            length += self.vocabluary[char]
            pass
        return length
        pass

    pass