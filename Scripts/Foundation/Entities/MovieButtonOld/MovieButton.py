from Foundation.ArrowManager import ArrowManager
from Foundation.Entity.BaseEntity import BaseEntity
from Notification import Notification

class MovieButton(BaseEntity):
    s_keys = dict(Esc=Mengine.KC_ESCAPE, Enter=Mengine.KC_RETURN)

    @staticmethod
    def declareORM(Type):
        BaseEntity.declareORM(Type)
        Type.addAction(Type, "IsAttachReact")
        Type.addAction(Type, "HintPoint")

        Type.addAction(Type, "ResourceMovieIdle")
        Type.addAction(Type, "ResourceMovieEnter")
        Type.addAction(Type, "ResourceMovieOver")
        Type.addAction(Type, "ResourceMovieClick")
        Type.addAction(Type, "ResourceMoviePressed")
        Type.addAction(Type, "ResourceMovieLeave")
        Type.addAction(Type, "ResourceMovieRelease")

        Type.addAction(Type, "Clickable")

        Type.addAction(Type, "SwitchMode", Update=MovieButton.__switchUpdate)

        Type.addAction(Type, "KeyTag")
        Type.addAction(Type, "BlockKeys")

        Type.addAction(Type, "Over")
        pass

    def __switchUpdate(self, value):
        if value is False:
            return
            pass
        if self.MoviePressed is None:
            Trace.log("MovieButton", 0, "MovieButton -->%s<-- is not support switch mode. Please add Movie_Pressed!!!!" % (self.object.getName()))
            pass
        pass

    def getHotSpot(self):
        if self.currentMovie is None:
            return self.MovieIdle.getSocket("socket")
            pass

        hotspot = self.currentMovie.getSocket("socket")
        return hotspot
        pass

    def __init__(self):
        super(MovieButton, self).__init__()
        self.MovieIdle = None
        self.MovieEnter = None
        self.MovieOver = None
        self.MovieClick = None
        self.MoviePressed = None
        self.MovieLeave = None
        self.MovieRelease = None

        self.currentMovie = None
        self.onKeyEventObserver = None
        pass

    def _updateInteractive(self, value):
        super(MovieButton, self)._updateInteractive(value)

        if value is True:
            self.object.setClickable(True)
            if self.SwitchMode is False:
                self.__cleanListeners(self.currentMovie)
                self.__onIdle()
                pass
            else:
                self.__switchOff()
                pass
            pass
        else:
            self.object.setClickable(False)
            if self.Over is True:
                self.setOver(True)
                pass
            pass
        pass

    def isMouseEnter(self):
        if self.currentMovie is None:
            return False
            pass
        hotspot = self.currentMovie.getSocket("socket")
        return hotspot.isMousePickerOver()
        pass

    def isSocketMouseEnter(self, movie):
        hotspot = movie.getSocket("socket")
        pickerOver = hotspot.isMousePickerOver()

        return pickerOver
        pass

    def setupMovie(self, resourceName):
        def __checkSocket(movie):
            if movie.hasSocket("socket") is False:
                Trace.log("Entity", 0, "MovieButton not initialized!!! Movie %s doesn't has socket:socket..." % (movie.getName(),))

                return None
                pass
            pass

        if Mengine.hasResource(resourceName) is False:
            return None
            pass

        resource = Mengine.getResourceReference(resourceName)
        Movie = self.createChild("Movie")
        Movie.setName(resourceName)
        Movie.setResourceMovie(resource)

        __checkSocket(Movie)

        return Movie
        pass

    def _onInitialize(self, obj):
        super(MovieButton, self)._onInitialize(obj)

        self.MovieIdle = self.setupMovie(self.ResourceMovieIdle)
        self.MovieEnter = self.setupMovie(self.ResourceMovieEnter)
        self.MovieOver = self.setupMovie(self.ResourceMovieOver)
        self.MovieClick = self.setupMovie(self.ResourceMovieClick)
        self.MoviePressed = self.setupMovie(self.ResourceMoviePressed)
        self.MovieLeave = self.setupMovie(self.ResourceMovieLeave)
        self.MovieRelease = self.setupMovie(self.ResourceMovieRelease)

        if self.MovieIdle is None:
            self.initializeFailed("MovieButton not initialized!!! Idle for %s was not setuped" % (self.object.getName(),))
            pass

        if self.MovieClick is None:
            self.initializeFailed("MovieButton not initialized!!! Click for %s was not setuped" % (self.object.getName(),))
            pass
        pass

    def __disableAll(self):
        if self.MovieEnter is not None:
            self.MovieEnter.disable()
            pass
        if self.MovieOver is not None:
            self.MovieOver.disable()
            pass
        if self.MovieClick is not None:
            self.MovieClick.disable()
            pass
        if self.MoviePressed is not None:
            self.MoviePressed.disable()
            pass
        if self.MovieLeave is not None:
            self.MovieLeave.disable()
            pass
        if self.MovieRelease is not None:
            self.MovieRelease.disable()
            pass
        if self.MovieIdle is not None:
            self.MovieIdle.disable()
            pass
        pass

    def _onPreparation(self):
        super(MovieButton, self)._onPreparation()
        self.__disableAll()
        pass

    def __cleanListeners(self, movie):
        if movie is None:
            return
            pass

        if movie.isEnable() is True:
            socket = movie.getSocket("socket")
            socket.setEventListener(onHandleMouseEnter=None,
                                    onHandleMouseLeave=None,
                                    onHandleMouseButtonEvent=None,
                                    onHandleKeyEvent=None)
            movie.setEventListener(onAnimatableEnd=None)
            movie.stop()
            movie.setFirstFrame()
            pass

        movie.disable()
        pass

    def _onActivate(self):
        super(MovieButton, self)._onActivate()
        if self.Over is False:
            self.__onIdle()
            pass
        else:
            self.setOver(True)
            pass
        pass

    def __onIdle(self):
        # Trace.trace()
        if self.Over is True:
            return
            pass

        self.MovieIdle.enable()
        self.MovieIdle.compile()
        socket = self.MovieIdle.getSocket("socket")
        socket.enable()
        socket.compile()
        if self.currentMovie != self.MovieIdle:
            self.__cleanListeners(self.currentMovie)
            self.setCurrentMovie(self.MovieIdle)
            pass

        if self.isSocketMouseEnter(self.MovieIdle) is True:
            if self.IsAttachReact is False:
                if ArrowManager.emptyArrowAttach() is False:
                    return
                    pass
                pass

            self.__onEnter()
            return
            pass

        self.MovieIdle.setLoop(True)
        self.MovieIdle.play()

        if self.Clickable is False:
            socket = self.MovieIdle.getSocket("socket")
            socket.disable()
            return
            pass

        socket.setEventListener(onHandleMouseEnter=self.__onIdleMouseEnter)
        if self.KeyTag is not None:
            socket.setEventListener(onHandleKeyEvent=self._onKeyEvent)
            pass
        pass

    def __onIdleMouseEnter(self, hs, x, y):
        if self.Clickable is False:
            return False
            pass
        if self.IsAttachReact is False:
            if ArrowManager.emptyArrowAttach() is False:
                return False
                pass
            pass

        self.__onEnter()
        return False
        pass

    def setCurrentMovie(self, movie):
        self.currentMovie = movie
        pass

    def __onEnter(self):
        Notification.notify(Notificator.onButtonMouseEnter, self.object)

        if self.MovieEnter is None:
            self.__onOver()
            return
            pass

        self.MovieEnter.enable()

        if self.currentMovie != self.MovieEnter:
            self.__cleanListeners(self.currentMovie)
            self.setCurrentMovie(self.MovieEnter)
            pass

        self.setCurrentMovie(self.MovieEnter)

        if self.isSocketMouseEnter(self.MovieEnter) is False:
            if self.IsAttachReact is False:
                if ArrowManager.emptyArrowAttach() is False:
                    return
                    pass
                pass

            self.__cleanListeners(self.MovieEnter)
            self.__onIdle()
            return
            pass

        self.MovieEnter.setEventListener(onAnimatableEnd=self.__onEnterMovieEnd)

        self.MovieEnter.play()
        socket = self.MovieEnter.getSocket("socket")

        socket.setEventListener(onHandleMouseButtonEvent=self.__onEnterMouseClick,
                                onHandleMouseLeave=self.__onOverMouseLeave)
        if self.KeyTag is not None:
            socket.setEventListener(onHandleKeyEvent=self._onKeyEvent)
            pass
        pass

    def __onEnterMouseClick(self, hs, touchId, x, y, button, isDown, isPressed):
        if isDown is False:
            return True
            pass

        if button != 0:
            return True
            pass

        self.__onClick()

        return True
        pass

    def __onEnterMovieEnd(self, emitter, id, isEnd):
        if self.currentMovie == self.MovieEnter:
            self.__onOver()
            pass
        else:
            self.__onIdle()
            pass
        pass

    def setOver(self, value):
        if self.MovieOver is None or value is False:
            return
            pass

        self.__cleanListeners(self.currentMovie)
        self.setCurrentMovie(self.MovieOver)
        self.MovieOver.enable()
        self.MovieOver.compile()
        pass

    def __onOver(self):
        if self.MovieOver is None:
            return
            pass

        self.__cleanListeners(self.currentMovie)

        self.setCurrentMovie(self.MovieOver)
        self.MovieOver.enable()

        if self.isSocketMouseEnter(self.MovieOver) is False:
            self.__cleanListeners(self.MovieOver)
            self.__onLeave()
            return
            pass

        self.MovieOver.setLoop(True)
        self.MovieOver.play()
        socket = self.MovieOver.getSocket("socket")

        socket.setEventListener(onHandleMouseLeave=self.__onOverMouseLeave,
                                onHandleMouseButtonEvent=self.__onOverMouseClick)
        if self.KeyTag is not None:
            socket.setEventListener(onHandleKeyEvent=self._onKeyEvent)
            pass
        pass

    def __onOverMouseLeave(self, hs):
        self.__cleanListeners(self.currentMovie)
        self.__onLeave()
        pass

    def __onOverMouseClick(self, hs, touchId, x, y, button, isDown):
        if isDown is False:
            return True
            pass

        if button != 0:
            return True
            pass

        self.__onClick()

        return True
        pass

    def __onClick(self):
        Notification.notify(Notificator.onButtonClick, self.object)

        self.MovieClick.enable()
        if self.currentMovie != self.MovieClick:
            self.__cleanListeners(self.currentMovie)
            self.setCurrentMovie(self.MovieClick)
            pass

        self.MovieClick.setEventListener(onAnimatableEnd=self.__onClickMovieEnd)
        self.MovieClick.play()
        pass

    def _onKeyEvent(self, hs, key, x, y, isDown, isRepeating):
        if self.KeyTag is None:
            return False
            pass

        if Mengine.isExclusiveKeyDown(key) is False:
            return False
            pass

        if isDown is False:
            return False
            pass

        if self.BlockKeys is True:
            return False
            pass

        KeyTag = MovieButton.s_keys[self.KeyTag]
        if KeyTag == key:
            if self.object.getEnable() is True:
                self.__onClick()
                pass
            pass

        return True
        pass

    def __onClickMovieEnd(self, emitter, id, isEnd):
        Notification.notify(Notificator.onButtonClickEnd, self.object)

        if self.SwitchMode is False:
            if self.MoviePressed is not None:
                self.__cleanListeners(self.MovieClick)
                self.__onPressed()
                pass

            self.__onClickWithoutPressed()
            pass
        elif self.SwitchMode is True:
            self.__cleanListeners(self.MovieClick)
            self.__onSwitch()
            pass
        pass

    def __onSwitch(self):
        Notification.notify(Notificator.onButtonSwitchOn, self.object)
        self.setCurrentMovie(self.MoviePressed)
        self.MovieEnter.setEventListener(onAnimatableEnd=self.__onEnterMovieEnd)
        self.MoviePressed.enable()
        self.MoviePressed.setLoop(True)
        self.MoviePressed.play()
        socket = self.MoviePressed.getSocket("socket")

        socket.setEventListener(onHandleMouseButtonEvent=self.__onSwitchMouseClick)

        if self.KeyTag is not None:
            socket.setEventListener(onHandleKeyEvent=self._onKeyEvent)
            pass
        pass

    def __onSwitchMouseClick(self, hs, touchId, x, y, button, isDown):
        if isDown is True:
            return True
            pass

        if button != 0:
            return True
            pass

        if self.Clickable is False:
            return False
            pass

        self.__switchOff()

        return True
        pass

    def __switchOff(self):
        Notification.notify(Notificator.onButtonSwitchOff, self.object)
        self.__cleanListeners(self.MoviePressed)
        self.__onRelease()
        pass

    def __onClickWithoutPressed(self):  # ---if MoviePressed doesn't exist
        self.MovieClick.setEventListener(onAnimatableEnd=None)

        if Mengine.isMouseButtonDown(0) is False:
            self.__cleanListeners(self.MovieClick)
            self.__onRelease()
            return
            pass

        self.setEventListener(onGlobalHandleMouseButtonEvent=self.__onGlobalHandleClickMouseButtonEvent)

        self.enableGlobalMouseEvent(True)
        pass

    def __onGlobalHandleClickMouseButtonEvent(self, en, touchId, button, isDown):
        if isDown is False:
            self.__cleanListeners(self.MovieClick)
            self.__onRelease()
            pass
        pass

    def __onPressed(self):
        self.setCurrentMovie(self.MoviePressed)
        self.MoviePressed.enable()

        if Mengine.isMouseButtonDown(0) is False:
            self.__cleanListeners(self.MoviePressed)
            self.__onRelease()
            return
            pass

        self.setEventListener(onGlobalHandleMouseButtonEvent=self.__onGlobalHandlePressedMouseButtonEvent)
        self.enableGlobalMouseEvent(True)

        self.MoviePressed.setLoop(True)
        self.MoviePressed.play()
        pass

    def __onGlobalHandlePressedMouseButtonEvent(self, en, touchId, button, isDown):
        if isDown is False:
            self.__cleanListeners(self.MoviePressed)
            self.__onRelease()
            pass
        pass

    def _hasUniqueKeyEvent(self):
        return True
        pass

    def __onOverClick(self):
        self.setCurrentMovie(self.MovieOver)
        self.MovieOver.enable()

        if self.isSocketMouseEnter(self.MovieOver) is False:
            self.__cleanListeners(self.MovieOver)
            self.__onIdle()
            return
            pass

        self.MovieOver.setLoop(True)
        self.MovieOver.play()
        socket = self.MovieOver.getSocket("socket")

        socket.setEventListener(onHandleMouseLeave=self.__onOverMouseLeave,
                                onHandleMouseButtonEvent=self.__onOverMouseClick)

        if self.KeyTag is not None:
            socket.setEventListener(onHandleKeyEvent=self._onKeyEvent)
            pass
        pass

    def __onRelease(self):
        self.enableGlobalMouseEvent(False)
        self.setEventListener(onGlobalHandleMouseButtonEvent=None)
        Notification.notify(Notificator.onButtonClickUp, self.object)

        if self.MovieRelease is None:
            self.__onOverClick()
            return
            pass

        self.setCurrentMovie(self.MovieRelease)

        self.MovieRelease.setEventListener(onAnimatableEnd=self.__onReleaseMovieEnd)
        self.MovieRelease.enable()
        self.MovieRelease.play()

        socket = self.MovieLeave.getSocket("socket")
        socket.setEventListener(onHandleMouseButtonEvent=self.__onReleaseMouseClick)

        if self.KeyTag is not None:
            socket.setEventListener(onHandleKeyEvent=self._onKeyEvent)
            pass
        pass

    def __onReleaseMouseClick(self, hs, touchId, x, y, button, isDown):
        if button != 0:
            return True
            pass

        if isDown is False:
            return True
            pass

        self.__cleanListeners(self.MovieRelease)
        self.__onClick()

        return True
        pass

    def __onReleaseMovieEnd(self, emitter, id, isEnd):
        self.__cleanListeners(self.MovieRelease)
        self.__onIdle()
        pass

    def __onLeave(self):
        Notification.notify(Notificator.onButtonMouseLeave, self.object)
        if self.MovieLeave is None:
            self.__onIdle()
            return
            pass

        self.setCurrentMovie(self.MovieLeave)
        self.MovieLeave.enable()
        self.MovieLeave.setEventListener(onAnimatableEnd=self.__onLeaveMovieEnd)
        self.MovieLeave.play()

        socket = self.MovieLeave.getSocket("socket")
        socket.setEventListener(onHandleMouseButtonEvent=self.__onLeaveMouseClick)

        if self.KeyTag is not None:
            socket.setEventListener(onHandleKeyEvent=self._onKeyEvent)
            pass
        pass

    def __onLeaveMouseClick(self, hs, touchId, x, y, button, isDown):
        if button != 0:
            return True
            pass

        if isDown is False:
            return True
            pass
        self.__onClick()

        return True
        pass

    def __onLeaveMovieEnd(self, emitter, id, isEnd):
        self.__cleanListeners(self.MovieLeave)
        self.__onIdle()
        pass

    def _onPreparationDeactivate(self):
        super(MovieButton, self)._onPreparationDeactivate()
        self.setCurrentMovie(None)
        self.enableGlobalMouseEvent(False)
        self.setEventListener(onGlobalHandleMouseButtonEvent=None)

        if self.onKeyEventObserver is not None:
            Notification.removeObserver(self.onKeyEventObserver)
            pass

        self.__cleanListeners(self.MovieEnter)
        self.__cleanListeners(self.MovieOver)
        self.__cleanListeners(self.MovieClick)
        self.__cleanListeners(self.MoviePressed)
        self.__cleanListeners(self.MovieLeave)
        self.__cleanListeners(self.MovieRelease)
        self.__cleanListeners(self.MovieIdle)
        pass

    def _onDeactivate(self):
        super(MovieButton, self)._onDeactivate()
        pass

    def _onFinalize(self):
        super(MovieButton, self)._onFinalize()
        pass
    pass