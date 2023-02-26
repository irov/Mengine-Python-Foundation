from Foundation.Entity.BaseEntity import BaseEntity
from Foundation.ObjectManager import ObjectManager
from Foundation.TaskManager import TaskManager

class MovieButton(BaseEntity):
    __metaclass__ = finalslots("tc", "state", "Movies", "SemaphoreBlock", "EventSkipState")

    @staticmethod
    def declareORM(Type):
        BaseEntity.declareORM(Type)
        Type.addAction(Type, "ResourceMovieIdle")
        Type.addAction(Type, "ResourceMovieEnter")
        Type.addAction(Type, "ResourceMovieOver")
        Type.addAction(Type, "ResourceMovieClick")
        Type.addAction(Type, "ResourceMovieLeave")

        Type.addAction(Type, "ResourceMoviePush")
        Type.addAction(Type, "ResourceMoviePressed")
        Type.addAction(Type, "ResourceMovieRelease")

        Type.addAction(Type, "ResourceMovieBlock")

        Type.addActionActivate(Type, "Block", Update=Type.__updateBlock)
        pass

    def __init__(self):
        super(MovieButton, self).__init__()
        self.tc = None
        self.state = "Idle"

        self.Movies = {}

        self.SemaphoreBlock = Semaphore(False, "MovieButtonBlock")

        self.EventSkipState = Event("SkipState")
        pass

    def __updateBlock(self, value):
        if value == True:
            self.SemaphoreBlock.setValue(True)
            return
            pass

        self.SemaphoreBlock.setValue(False)
        pass

    def getCurrentMovie(self):
        if self.state not in self.Movies:
            return None
            pass

        Movie = self.Movies[self.state]

        if Movie is None:
            return None

        return Movie
        pass

    def getCurrentMovieSocketCenter(self):
        movie = self.getCurrentMovie()

        if movie is not None:
            socket = movie.getSocket('socket')
            center_position = socket.getWorldPolygonCenter()

            return center_position

    def _onInitialize(self, obj):
        super(MovieButton, self)._onInitialize(obj)

        def __createMovie(name, res, play, loop):
            if res is None:
                return None
                pass

            if Menge.hasResource(res) is False:
                return False
                pass

            resource = Menge.getResourceReference(res)

            if resource is None:
                Trace.log("Entity", 0, "MovieButton._onInitialize: not found resource %s" % (res))
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

        __createMovie("Idle", self.ResourceMovieIdle, True, True)
        __createMovie("Over", self.ResourceMovieOver, True, True)

        __createMovie("Enter", self.ResourceMovieEnter, False, False)
        __createMovie("Leave", self.ResourceMovieLeave, False, False)

        __createMovie("Click", self.ResourceMovieClick, False, False)

        __createMovie("Push", self.ResourceMoviePush, False, False)
        __createMovie("Release", self.ResourceMovieRelease, False, False)
        __createMovie("Pressed", self.ResourceMoviePressed, True, True)

        __createMovie("Block", self.ResourceMovieBlock, True, True)

        return True
        pass

    def __setState(self, state):
        self.state = state
        pass

    def __stateIdle(self, source, MovieIdle):
        source.addEnable(MovieIdle)
        source.addDelay(0.0)
        with source.addRaceTask(3) as (source_over_click, source_over_enter, source_block):
            source_over_click.addTask("TaskMovieSocketClick", SocketName="socket", Movie=MovieIdle, isDown=True)
            source_over_click.addFunction(self.__setState, "Push")

            source_over_enter.addTask("TaskMovieSocketEnter", SocketName="socket", Movie=MovieIdle)
            source_over_enter.addFunction(self.__setState, "Enter")

            source_block.addSemaphore(self.SemaphoreBlock, From=True)
            source_block.addFunction(self.__setState, "Block")
            pass

        source.addDisable(MovieIdle)
        pass

    def __stateOver(self, source, MovieOver):
        if MovieOver is None:
            source.addFunction(self.__setState, "Push")
            return
            pass

        source.addEnable(MovieOver)
        source.addDelay(0.0)

        with source.addRaceTask(3) as (source_over_click, source_over_leave, source_block):
            source_over_click.addTask("TaskMovieSocketClick", SocketName="socket", Movie=MovieOver, isDown=True, Already=True)
            source_over_click.addFunction(self.__setState, "Push")

            source_over_leave.addTask("TaskMovieSocketLeave", SocketName="socket", Movie=MovieOver)
            source_over_leave.addFunction(self.__setState, "Leave")

            source_block.addSemaphore(self.SemaphoreBlock, From=True)
            source_block.addFunction(self.__setState, "Block")
            pass

        source.addDisable(MovieOver)
        pass

    def __stateEnter(self, source, MovieEnter):
        if MovieEnter is None:
            source.addTask("TaskNotify", ID=Notificator.onButtonMouseEnter, Args=(self.object,))
            source.addTask("TaskNotify", ID=Notificator.onMovieButtonMouseEnter, Args=(self.object,))
            source.addFunction(self.__setState, "Over")
            return
            pass

        source.addEnable(MovieEnter)
        source.addDelay(0.0)
        source.addTask("TaskNotify", ID=Notificator.onButtonMouseEnter, Args=(self.object,))
        source.addTask("TaskNotify", ID=Notificator.onMovieButtonMouseEnter, Args=(self.object,))

        with source.addRaceTask(3) as (source_enter_movie, source_enter_leave, source_enter_click):
            source_enter_movie.addTask("TaskMoviePlay", Movie=MovieEnter)
            source_enter_movie.addFunction(self.__setState, "Over")

            source_enter_leave.addTask("TaskMovieSocketLeave", SocketName="socket", Movie=MovieEnter)
            source_enter_leave.addFunction(self.__setState, "Idle")

            source_enter_click.addTask("TaskMovieSocketClick", SocketName="socket", Movie=MovieEnter, isDown=True, Already=True)
            source_enter_click.addFunction(self.__setState, "Push")
            pass

        source.addDisable(MovieEnter)
        pass

    def __stateLeave(self, source, MovieLeave):
        if MovieLeave is None:
            source.addTask("TaskNotify", ID=Notificator.onMovieButtonMouseLeave, Args=(self.object,))
            source.addFunction(self.__setState, "Idle")
            return
            pass

        source.addEnable(MovieLeave)
        source.addDelay(0.0)
        source.addTask("TaskNotify", ID=Notificator.onMovieButtonMouseLeave, Args=(self.object,))

        with source.addRaceTask(2) as (source_leave_movie, source_leave_enter):
            source_leave_movie.addTask("TaskMoviePlay", Movie=MovieLeave)
            source_leave_movie.addFunction(self.__setState, "Idle")

            source_leave_enter.addTask("TaskMovieSocketEnter", SocketName="socket", Movie=MovieLeave)
            source_leave_enter.addFunction(self.__setState, "Over")
            pass

        source.addDisable(MovieLeave)
        pass

    def __statePush(self, source, MoviePush):
        if MoviePush is None:
            source.addTask("TaskNotify", ID=Notificator.onMovieButtonPush, Args=(self.object,))
            source.addFunction(self.__setState, "Pressed")
            return
            pass

        source.addEnable(MoviePush)
        source.addTask("TaskNotify", ID=Notificator.onMovieButtonPush, Args=(self.object,))
        source.addDelay(0.0)

        with source.addRaceTask(3) as (source_Push_movie, source_Push_leave, source_Pressed_click_Rel):
            source_Push_movie.addTask("TaskMoviePlay", Movie=MoviePush)
            source_Push_movie.addFunction(self.__setState, "Pressed")

            source_Push_leave.addTask("TaskMovieSocketLeave", SocketName="socket", Movie=MoviePush)
            source_Push_leave.addFunction(self.__setState, "Release")

            source_Pressed_click_Rel.addTask("TaskMovieSocketClick", SocketName="socket", Movie=MoviePush, isDown=False, Already=True)
            source_Pressed_click_Rel.addFunction(self.__setState, "Click")
            pass

        source.addDisable(MoviePush)
        pass

    def __statePressed(self, source, MoviePressed):
        if MoviePressed is None:
            source.addFunction(self.__setState, "Click")
            return
            pass

        source.addEnable(MoviePressed)
        source.addDelay(0.0)
        source.addNotify(Notificator.onMovieButtonPressed, self.object)

        with source.addRaceTask(3) as (source_Pressed_click_Rel, source_Pressed_leave, source_block):
            source_Pressed_click_Rel.addTask("TaskMovieSocketClick", SocketName="socket", Movie=MoviePressed, isDown=False, isPressed=False, Already=True)
            source_Pressed_click_Rel.addFunction(self.__setState, "Click")

            source_Pressed_leave.addTask("TaskMovieSocketLeave", SocketName="socket", Movie=MoviePressed)
            source_Pressed_leave.addFunction(self.__setState, "Release")

            source_block.addSemaphore(self.SemaphoreBlock, From=True)
            source_block.addFunction(self.__setState, "Block")
            pass

        source.addDisable(MoviePressed)
        pass

    def __stateRelease(self, source, MoviePressed):
        if MoviePressed is None:
            source.addTask("TaskNotify", ID=Notificator.onMovieButtonRelease, Args=(self.object,))
            source.addFunction(self.__setState, "Release_Play")
            return
            pass

        source.addEnable(MoviePressed)
        source.addTask("TaskNotify", ID=Notificator.onMovieButtonRelease, Args=(self.object,))
        source.addDelay(0.0)

        with source.addRaceTask(2) as (source_Release_movie, source_Release_enter):
            source_Release_movie.addTask("TaskMouseButtonClick", isDown=False)
            source_Release_enter.addFunction(self.__setState, "Release_Play")

            source_Release_enter.addTask("TaskMovieSocketEnter", SocketName="socket", Movie=MoviePressed)
            source_Release_enter.addFunction(self.__setState, "Pressed")
            pass

        source.addDisable(MoviePressed)
        pass

    def __stateReleasePlay(self, source, MovieRelease):
        if MovieRelease is None:
            source.addFunction(self.__setState, "Idle")
            return
            pass

        source.addEnable(MovieRelease)
        source.addTask("TaskMoviePlay", Movie=MovieRelease)
        source.addFunction(self.__setState, "Idle")
        source.addDisable(MovieRelease)
        pass

    def __stateClick(self, source, MovieClick):
        if MovieClick is None:
            source.addTask("TaskNotify", ID=Notificator.onButtonClickBegin, Args=(self.object,))
            source.addTask("TaskNotify", ID=Notificator.onButtonClick, Args=(self.object,))
            source.addTask("TaskNotify", ID=Notificator.onMovieButtonClick, Args=(self.object,))
            source.addTask("TaskNotify", ID=Notificator.onMovieButtonClickEnd, Args=(self.object,))
            source.addFunction(self.__setState, "Idle")
            return
            pass

        source.addEnable(MovieClick)
        source.addTask("TaskNotify", ID=Notificator.onButtonClickBegin, Args=(self.object,))
        source.addTask("TaskNotify", ID=Notificator.onButtonClick, Args=(self.object,))
        source.addTask("TaskNotify", ID=Notificator.onMovieButtonClick, Args=(self.object,))
        source.addTask("TaskMoviePlay", Movie=MovieClick)
        source.addTask("TaskNotify", ID=Notificator.onMovieButtonClickEnd, Args=(self.object,))
        source.addFunction(self.__setState, "Idle")
        source.addDisable(MovieClick)
        pass

    def __stateBlock(self, source, MovieBlock):
        if MovieBlock is None:
            source.addSemaphore(self.SemaphoreBlock, From=False)
            source.addFunction(self.__setState, "Idle")
            return
            pass

        source.addEnable(MovieBlock)

        source.addSemaphore(self.SemaphoreBlock, From=False)
        source.addFunction(self.__setState, "Idle")

        source.addDisable(MovieBlock)
        pass

    def setState(self, state):
        states = ("Idle", "Enter", "Leave", "Over", "Click", "Push", "Pressed", "Release", "Block")
        if state not in states:
            return

        self.__setState(state)
        self.EventSkipState()

    def scopeDisableAllMovies(self, source):
        for Movie in self.Movies.itervalues():
            if Movie is None:
                continue

            source.addDisable(Movie)

    def getStateMovie(self, state):
        touchpad_ignore = ["Enter", "Over", "Leave", "Release"]
        defaults = {"Over": "Idle", "Pressed": "Idle", "Block": "Idle", }
        default_state_name = defaults.get(state)
        movie_default = self.Movies.get(default_state_name)
        movie_state = self.Movies.get(state, movie_default)

        if Menge.hasTouchpad() is True and state in touchpad_ignore:
            # mobile devices don't have this states - use default or nothing
            return movie_default

        return movie_state

    def _onActivate(self):
        super(MovieButton, self)._onActivate()

        MovieIdle = self.getStateMovie("Idle")
        MovieEnter = self.getStateMovie("Enter")
        MovieLeave = self.getStateMovie("Leave")
        MovieOver = self.getStateMovie("Over")
        MovieClick = self.getStateMovie("Click")
        MoviePush = self.getStateMovie("Push")
        MoviePressed = self.getStateMovie("Pressed")
        MovieRelease = self.getStateMovie("Release")
        MovieBlock = self.getStateMovie("Block")

        self.state = "Idle"

        self.tc = TaskManager.createTaskChain(Repeat=True, NoCheckAntiStackCycle=True)

        with self.tc as source_repeat:
            Scopes = dict(Idle=Functor(self.__stateIdle, MovieIdle), Enter=Functor(self.__stateEnter, MovieEnter), Over=Functor(self.__stateOver, MovieOver), Leave=Functor(self.__stateLeave, MovieLeave), Click=Functor(self.__stateClick, MovieClick), Push=Functor(self.__statePush, MoviePush), Pressed=Functor(self.__statePressed, MoviePressed), Release=Functor(self.__stateRelease, MovieRelease), Release_Play=Functor(self.__stateReleasePlay, MovieRelease),

                Block=Functor(self.__stateBlock, MovieBlock), )

            def __states(isSkip, cb):
                cb(isSkip, self.state)
                pass

            # - new ------------------------------------------------------------------
            with source_repeat.addRaceTask(2) as (source_switch, source_skip):
                source_switch.addScopeSwitch(Scopes, __states)

                source_skip.addEvent(self.EventSkipState)
                source_skip.addScope(self.scopeDisableAllMovies)
            # ------------------------------------------------------------------------

            # source_repeat.addScopeSwitch(Scopes, __states)

            # with tc_repeat.addSwitchTask(len(MovieButton.States), __states) as sources:
            #     sources[MovieButton.States.index("Idle")].addScope(self.__stateIdle, MovieIdle)
            #     sources[MovieButton.States.index("Enter")].addScope(self.__stateEnter, MovieEnter)
            #     sources[MovieButton.States.index("Over")].addScope(self.__stateOver, MovieOver)
            #     sources[MovieButton.States.index("Leave")].addScope(self.__stateLeave, MovieLeave)
            #     sources[MovieButton.States.index("Click")].addScope(self.__stateClick, MovieClick)
            #
            #     sources[MovieButton.States.index("Push")].addScope(self.__statePush, MoviePush)
            #     sources[MovieButton.States.index("Pressed")].addScope(self.__statePressed, MoviePressed)
            #     sources[MovieButton.States.index("Release")].addScope(self.__stateRelease, MovieRelease)
            #     sources[MovieButton.States.index("Release_Play")].addScope(self.__stateReleasePlay, MovieRelease)
            #     pass
            pass
        pass

    def _onDeactivate(self):
        super(MovieButton, self)._onDeactivate()

        if self.tc is not None:
            self.tc.cancel()
            self.tc = None
            pass

        for mov in self.Movies.itervalues():
            mov.setEnable(False)
            pass
        pass

    def _onFinalize(self):
        super(MovieButton, self)._onFinalize()

        for mov in self.Movies.itervalues():
            mov.onDestroy()
            pass

        self.Movies = {}
        pass
    pass