class MovieButtonState(object):
    s_keys = dict(Esc=Mengine.KC_ESCAPE, Enter=Mengine.KC_RETURN)

    def __init__(self):
        super(MovieButtonState, self).__init__()
        self.buttonEntity = None
        self.movie = None
        self.socket = None
        self.DefaultNextState = None
        self.stateClick = False
        self.stateEnter = None
        self.changed = None
        pass

    def onParams(self, buttonEntity, resourceName):
        self.buttonEntity = buttonEntity
        self.movie = self.setupMovie(resourceName)
        pass

    def getMovie(self):
        return self.movie
        pass

    def setupMovie(self, resourceName):
        def __checkSocket(movie):
            if movie.hasSocket("socket") is False:
                Trace.log("Entity", 0, "MovieButton %s in group %s not initialized!!! Movie %s doesn't has socket:socket..." % (self.buttonEntity.object.getName(), self.buttonEntity.object.getGroupName(), movie.getName(),))

                return None
                pass
            pass

        if Mengine.hasResource(resourceName) is False:
            Trace.log("Entity", 0, "MovieButton %s in group %s not initialized!!! Doesn't exist resource %s (maybe not correct composition name in aep)" % (self.buttonEntity.object.getName(), self.buttonEntity.object.getGroupName(), resourceName,))
            return None
            pass

        resource = Mengine.getResourceReference(resourceName)
        Movie = Mengine.createNode("Movie")
        Movie.setName(resourceName)
        Movie.setResourceMovie(resource)

        self.buttonEntity.addChild(Movie)

        __checkSocket(Movie)
        return Movie
        pass

    def isSocketMouseEnter(self):
        hotspot = self.movie.getSocket("socket")
        pickerOver = hotspot.isMousePickerOver()

        return pickerOver
        pass

    def updateClickable(self):
        self._updateClickable()
        pass

    def _updateClickable(self):
        pass

    def disable(self):
        if self.movie is None:
            return
            pass

        self.movie.disable()
        pass

    def enable(self):
        self.movie.enable()
        self.movie.compile()
        self.movie.play()

        self.socket = self.movie.getSocket("socket")
        self.socket.enable()
        pass

    def activate(self):
        activated = self._activate()

        if activated is False:
            return
            pass

        self.socket.setEventListener(onHandleMouseEnter=self.onMouseEnter, onHandleMouseLeave=self.onMouseLeave, onHandleMouseButtonEvent=self.onMouseButtonEvent, onHandleKeyEvent=self.onKeyEvent)
        self.movie.setEventListener(onAnimatableEnd=self.onMovieEnd)
        pass

    def _activate(self):
        pass

    def setChanged(self, value):
        self.changed = value
        pass

    def deactivate(self):
        self.stateClick = False
        self.stateEnter = None
        self.setChanged(False)
        self._deactivate()

        if self.movie is None:
            return
            pass

        self.socket.setEventListener(onHandleMouseEnter=None, onHandleMouseLeave=None, onHandleMouseButtonEvent=None, onHandleKeyEvent=None)
        self.movie.setEventListener(onAnimatableEnd=None)
        self.movie.stop()
        self.movie.setFirstFrame()

        self.movie.disable()
        pass

    def _deactivate(self):
        pass

    def changeState(self):
        if self.changed is True:
            return
            pass

        self.setChanged(True)
        if self.stateClick is True:
            self.buttonEntity.changeState("Click")
            pass
        elif self.stateEnter is True:
            self.buttonEntity.changeState("Enter")
            pass
        elif self.stateEnter is False:
            self.buttonEntity.changeState("Leave")
            pass
        else:
            self.buttonEntity.changeState(self.DefaultNextState)
            pass
        pass

    def onMouseEnter(self, context, event):
        if self.buttonEntity.Clickable is False:
            return False
            pass

        self._onMouseEnter()

        return self.buttonEntity.Block

    def _onMouseEnter(self):
        pass

    def onMouseLeave(self, context, event):
        if self.buttonEntity.Clickable is False:
            return
            pass

        self._onMouseLeave()
        pass

    def _onMouseLeave(self):
        pass

    def onMouseButtonEvent(self, context, event):
        if event.isDown is False:
            return False
            pass

        if event.button != 0:
            return False
            pass

        if self.buttonEntity.Clickable is False:
            return False
            pass

        Block = self.buttonEntity.Block

        self._onMouseButtonEvent()

        return Block
        pass

    def _onMouseButtonEvent(self):
        pass

    def onKeyEvent(self, context, event):
        if self.buttonEntity.KeyTag is None:
            return False

        if Mengine.isExclusiveKeyDown(event.code) is False:
            return False

        if event.isDown is False:
            return False

        if self.buttonEntity.Clickable is False:
            return False

        KeyTag = MovieButtonState.s_keys[self.buttonEntity.KeyTag]

        if KeyTag == event.code:
            if self.buttonEntity.object.getEnable() is True:
                self._onKeyEvent()
                return self.buttonEntity.Block
            pass

        return False

    def _onKeyEvent(self):
        pass

    def onMovieEnd(self, emitter, id, isEnd):
        self._onMovieEnd()
        pass

    def _onMovieEnd(self):
        pass

    pass