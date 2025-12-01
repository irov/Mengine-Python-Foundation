from Event import Event
from Foundation.Entity.BaseEntity import BaseEntity
from Foundation.Notificator import Notificator
from Foundation.ObjectManager import ObjectManager
from Foundation.Task.Semaphore import Semaphore
from Foundation.TaskManager import TaskManager
from Functor import Functor
from Multislots import finalslots

class Movie2Button(BaseEntity):
    __metaclass__ = finalslots("tc", "state", "custom", "Movies", "SlotsChildren", "SemaphoreBlock",
                               "SemaphoreSelected", "EventSkipState", "EventSetState")

    s_keys = dict(Esc=Mengine.KC_ESCAPE, Enter=Mengine.KC_RETURN, False=False)

    @staticmethod
    def declareORM(Type):
        BaseEntity.declareORM(Type)

        Type.addAction("ResourceMovie")
        Type.addAction("CompositionNameIdle")
        Type.addAction("CompositionNameAppear")
        Type.addAction("CompositionNameEnter")
        Type.addAction("CompositionNameOver")
        Type.addAction("CompositionNameClick")
        Type.addAction("CompositionNameLeave")

        Type.addAction("CompositionNamePush")
        Type.addAction("CompositionNamePressed")
        Type.addAction("CompositionNameRelease")

        Type.addAction("CompositionNameBlock")
        Type.addAction("CompositionNameBlockEnter")
        Type.addAction("CompositionNameBlockEnd")

        Type.addAction("CompositionNameSelected")
        Type.addAction("CompositionNameSelectedEnter")
        Type.addAction("CompositionNameSelectedEnd")

        Type.addActionActivate("Block", Update=Type.__updateBlock)
        Type.addActionActivate("Selected", Update=Type.__updateSelected)

        Type.addAction("BlockKeys")
        Type.addAction("KeyTag")
        Type.addAction("Synchronize")

    def __init__(self):
        super(Movie2Button, self).__init__()
        self.tc = None
        self.state = "Appear"
        self.custom = False

        self.Movies = {}
        self.SlotsChildren = {}

        self.SemaphoreBlock = Semaphore(False, "Movie2ButtonBlock")
        self.SemaphoreSelected = Semaphore(False, "Movie2ButtonSelected")

        self.EventSkipState = Event("SkipState")
        self.EventSetState = Event("SetState")

    def hasSlot(self, slot_name):
        for movie in self.Movies.values():
            if movie is None:
                continue
            if movie.hasMovieSlot(slot_name):
                return True
        return False

    def addChildToSlot(self, node, slot_name):
        """ Attach node to slot with correct displaying """
        current_movie = self.getCurrentMovie()

        if current_movie is not None:
            if current_movie.hasSlot(slot_name) is False:
                if self.hasSlot(slot_name) is False:
                    Trace.log("Entity", 0, "Movie2Button.addChildToSlot: slot {!r} not found for {!r}, "
                                           "add it at least on one movie".format(slot_name, self.getName()))
                    return False
            else:
                slot = current_movie.getMovieSlot(slot_name)
                slot.addChild(node)

        if slot_name not in self.SlotsChildren:
            self.SlotsChildren[slot_name] = []
        if node not in self.SlotsChildren[slot_name]:
            self.SlotsChildren[slot_name].append(node)

        return True

    def __checkSlotChildren(self, node, slot_name):
        if slot_name not in self.SlotsChildren:
            Trace.log("Entity", 0, "slot {!r} never used via addChildToSlot".format(slot_name))
            return False

        if node not in self.SlotsChildren[slot_name]:
            Trace.log("Entity", 0, "node {!r} wasn't attached to slot {!r} "
                                   "via addChildToSlot".format(node.getName(), slot_name))
            return False
        return True

    def removeFromParentSlot(self, node, slot_name):
        """ Correct node.removeFromParent in Movie2Button case """
        if self.__checkSlotChildren(node, slot_name) is False:
            return False

        node.removeFromParent()
        self.SlotsChildren[slot_name].remove(node)
        return True

    def returnToParentFromSlot(self, entity, slot_name):
        """ Correct entity.returnToParent in Movie2Button case """
        entity_node = entity.getEntityNode()
        if self.__checkSlotChildren(entity_node, slot_name) is False:
            return False

        entity.returnToParent()
        self.SlotsChildren[slot_name].remove(entity_node)
        return True

    def __updateSlotsChildren(self):
        """ Reattach children to correct slot for current state is it possible """
        current_movie = self.getCurrentMovie()
        if current_movie is None:
            return True

        for slot_name, node_list in self.SlotsChildren.items():
            if current_movie.hasSlot(slot_name) is False:
                continue
            slot = current_movie.getMovieSlot(slot_name)

            for node in node_list:
                slot.addChild(node)
        return True

    def getCompositionBounds(self):
        current_movie = self.getCurrentMovie()

        if current_movie is None:
            current_movie = self.getStateMovie('Idle')

        return current_movie.getCompositionBounds()

    def hasCompositionBounds(self):
        current_movie = self.getCurrentMovie()

        if current_movie is None:
            current_movie = self.getStateMovie('Idle')

        return current_movie.hasCompositionBounds()

    def __updateBlock(self, value):
        if value is True:
            self.SemaphoreBlock.setValue(True)
            self.SemaphoreSelected.setValue(False)
            return
        self.SemaphoreBlock.setValue(False)

    def __updateSelected(self, value):
        if value is True:
            self.SemaphoreSelected.setValue(True)
            self.SemaphoreBlock.setValue(False)
            return
        self.SemaphoreSelected.setValue(False)

    def getCurrentMovie(self):
        if self.state not in self.Movies:
            return None

        Movie = self.getStateMovie(self.state)

        return Movie

    def getCurrentMovieSocketCenter(self):
        current_movie = self.getCurrentMovie() or self.getStateMovie("Idle")
        if current_movie is None:
            return None

        socket = current_movie.getSocket("socket")
        if socket is None:
            return None

        center_position = socket.getWorldPolygonCenter()
        return center_position

    def _onInitialize(self, obj):
        super(Movie2Button, self)._onInitialize(obj)

        if self.ResourceMovie is None:
            return False

        if Mengine.hasResource(self.ResourceMovie) is False:
            return False

        resource = Mengine.getResourceReference(self.ResourceMovie)

        if resource is None:
            Trace.log("Entity", 0, "Movie2Button._onInitialize: not found resource %s" % resource)
            return False

        def __createMovie2(name, comp, play, loop):
            if resource.hasComposition(comp) is False:
                return None

            mov = ObjectManager.createObjectUnique("Movie2", name, self.object, ResourceMovie=resource, CompositionName=comp)
            mov.setEnable(False)
            mov.setPlay(play)
            mov.setLoop(loop)
            mov.setInteractive(True)

            movEntityNode = mov.getEntityNode()
            self.addChild(movEntityNode)

            self.Movies[name] = mov

            return mov

        __createMovie2("Appear", self.CompositionNameAppear, False, False)
        __createMovie2("Idle", self.CompositionNameIdle, True, True)
        __createMovie2("Over", self.CompositionNameOver, True, True)

        __createMovie2("Enter", self.CompositionNameEnter, False, False)
        __createMovie2("Leave", self.CompositionNameLeave, False, False)

        __createMovie2("Click", self.CompositionNameClick, False, False)

        __createMovie2("Push", self.CompositionNamePush, False, False)
        __createMovie2("Release", self.CompositionNameRelease, False, False)
        __createMovie2("Pressed", self.CompositionNamePressed, True, True)

        __createMovie2("Block", self.CompositionNameBlock, True, True)
        __createMovie2("BlockEnter", self.CompositionNameBlockEnter, True, False)
        __createMovie2("BlockEnd", self.CompositionNameBlockEnd, True, False)

        __createMovie2("Selected", self.CompositionNameSelected, True, True)
        __createMovie2("SelectedEnter", self.CompositionNameSelectedEnter, True, False)
        __createMovie2("SelectedEnd", self.CompositionNameSelectedEnd, True, False)

        if "Appear" not in self.Movies:
            self.state = "Idle"

        return True

    def _onFinalize(self):
        super(Movie2Button, self)._onFinalize()

        self.SemaphoreBlock = None
        self.SemaphoreSelected = None

        self.EventSkipState = None
        self.EventSetState = None

        for mov in self.Movies.itervalues():
            mov.onDestroy()

        self.Movies = {}
        self.SlotsChildren = {}

    def __scopeEnable(self, source, movie):
        """ Used for correct displaying children on button slots """
        source.addFunction(self.__updateSlotsChildren)
        source.addEnable(movie)

    def __setState(self, state):
        Proportion = 0.0

        if self.Synchronize is True:
            current_state_movie = self.getCurrentMovie()

            if current_state_movie is None:
                current_state_movie = self.getStateMovie('Idle')

            Proportion = current_state_movie.getTimingProportion()
            pass

        self.EventSetState(self.state, state)

        self.state = state
        self.custom = False

        if self.Synchronize is True:
            current_state_movie = self.getCurrentMovie()

            if current_state_movie is None:
                current_state_movie = self.getStateMovie('Idle')

            current_state_movie.setTimingProportion(Proportion)
            Time = current_state_movie.getTimeFromProportion(Proportion)
            current_state_movie.setStartTiming(Time)

    def __stateAppear(self, source, MovieAppear):
        if MovieAppear is None:
            source.addFunction(self.__setState, "Idle")
            return

        source.addScope(self.__scopeEnable, MovieAppear)
        source.addDelay(0.0)

        with source.addIfTask(self.object.getEnable) as (source_true, source_false):
            source_false.addBlock()

        with source.addRaceTask(6) as (source_over_click, source_over_enter, source_block,
                                       source_selected, source_key, source_play):
            source_over_click.addTask("TaskMovie2SocketClick", SocketName="socket", Movie2=MovieAppear, isDown=True)
            source_over_click.addFunction(self.__setState, "Push")

            source_over_enter.addTask("TaskMovie2SocketEnter", SocketName="socket", Movie2=MovieAppear, isDown=False)
            source_over_enter.addFunction(self.__setState, "Enter")

            source_block.addSemaphore(self.SemaphoreBlock, From=True)
            source_block.addFunction(self.__setState, "BlockEnter")

            source_selected.addSemaphore(self.SemaphoreSelected, From=True)
            source_selected.addFunction(self.__setState, "SelectedEnter")

            source_key.addTask("TaskKeyPress", Keys=[Movie2Button.s_keys[self.KeyTag]])
            source_key.addFunction(self.__setState, "Click")

            source_play.addTask("TaskMovie2Play", Movie2=MovieAppear, Wait=True)
            source_play.addFunction(self.__setState, "Idle")

        source.addDisable(MovieAppear)

    def __stateIdle(self, source, MovieIdle):
        if MovieIdle is None:
            Trace.log("Entity", 0, "Group '%s' Movie2Button '%s': state Idle not found" % (
                self.object.getGroupName(), self.getName()))
            return

        source.addScope(self.__scopeEnable, MovieIdle)
        source.addDelay(0.0)

        with source.addRaceTask(5) as (source_over_click, source_over_enter, source_block, source_selected, source_key):
            source_over_click.addTask("TaskMovie2SocketClick", SocketName="socket", Movie2=MovieIdle, isDown=True)
            source_over_click.addFunction(self.__setState, "Push")

            source_over_enter.addTask("TaskMovie2SocketEnter", SocketName="socket", Movie2=MovieIdle, isDown=False)
            source_over_enter.addFunction(self.__setState, "Enter")

            source_block.addSemaphore(self.SemaphoreBlock, From=True)
            source_block.addFunction(self.__setState, "BlockEnter")

            source_selected.addSemaphore(self.SemaphoreSelected, From=True)
            source_selected.addFunction(self.__setState, "SelectedEnter")

            source_key.addTask("TaskKeyPress", Keys=[Movie2Button.s_keys[self.KeyTag]])
            source_key.addFunction(self.__setState, "Click")

        source.addDisable(MovieIdle)

    def __stateOver(self, source, MovieOver):
        if MovieOver is None:
            source.addFunction(self.__setState, "Push")
            return

        source.addScope(self.__scopeEnable, MovieOver)
        source.addDelay(0.0)

        with source.addRaceTask(5) as (source_over_click, source_over_leave, source_block, source_selected, source_key):
            source_over_click.addTask("TaskMovie2SocketClick", SocketName="socket",
                                      Movie2=MovieOver, isDown=True, Already=True)
            source_over_click.addFunction(self.__setState, "Push")

            source_over_leave.addTask("TaskMovie2SocketLeave", SocketName="socket", Movie2=MovieOver)
            source_over_leave.addFunction(self.__setState, "Leave")

            source_block.addSemaphore(self.SemaphoreBlock, From=True)
            source_block.addFunction(self.__setState, "BlockEnter")

            source_selected.addSemaphore(self.SemaphoreSelected, From=True)
            source_selected.addFunction(self.__setState, "SelectedEnter")

            source_key.addTask("TaskKeyPress", Keys=[Movie2Button.s_keys[self.KeyTag]])
            source_key.addFunction(self.__setState, "Click")

        source.addDisable(MovieOver)

    def __stateEnter(self, source, MovieEnter):
        if MovieEnter is None:
            source.addNotify(Notificator.onButtonMouseEnter, self.object)
            source.addNotify(Notificator.onMovie2ButtonMouseEnter, self.object)
            source.addFunction(self.__setState, "Over")
            return

        source.addScope(self.__scopeEnable, MovieEnter)
        source.addDelay(0.0)
        source.addNotify(Notificator.onButtonMouseEnter, self.object)
        source.addNotify(Notificator.onMovie2ButtonMouseEnter, self.object)

        with source.addRaceTask(3) as (source_enter_movie, source_enter_leave, source_enter_click):
            source_enter_movie.addTask("TaskMovie2Play", Movie2=MovieEnter)
            source_enter_movie.addFunction(self.__setState, "Over")

            source_enter_leave.addTask("TaskMovie2SocketLeave", SocketName="socket", Movie2=MovieEnter)
            source_enter_leave.addNotify(Notificator.onMovie2ButtonMouseLeave, self.object)
            source_enter_leave.addFunction(self.__setState, "Idle")

            source_enter_click.addTask("TaskMovie2SocketClick", SocketName="socket",
                                       Movie2=MovieEnter, isDown=True, Already=True)
            source_enter_click.addFunction(self.__setState, "Push")

        source.addDisable(MovieEnter)

    def __stateLeave(self, source, MovieLeave):
        if MovieLeave is None:
            source.addNotify(Notificator.onMovie2ButtonMouseLeave, self.object)
            source.addFunction(self.__setState, "Idle")
            return

        source.addScope(self.__scopeEnable, MovieLeave)
        source.addDelay(0.0)
        source.addNotify(Notificator.onMovie2ButtonMouseLeave, self.object)

        with source.addRaceTask(2) as (source_leave_movie, source_leave_enter):
            source_leave_movie.addTask("TaskMovie2Play", Movie2=MovieLeave)
            source_leave_movie.addFunction(self.__setState, "Idle")

            source_leave_enter.addTask("TaskMovie2SocketEnter", SocketName="socket", Movie2=MovieLeave)
            source_leave_enter.addFunction(self.__setState, "Enter")

        source.addDisable(MovieLeave)

    def __statePush(self, source, MoviePush):
        if MoviePush is None:
            source.addNotify(Notificator.onMovie2ButtonPush, self.object)
            source.addFunction(self.__setState, "Pressed")
            return

        source.addScope(self.__scopeEnable, MoviePush)
        source.addNotify(Notificator.onMovie2ButtonPush, self.object)
        source.addDelay(0.0)

        with source.addRaceTask(3) as (source_push_movie, source_push_leave, source_pressed_click_rel):
            source_push_movie.addTask("TaskMovie2Play", Movie2=MoviePush)
            source_push_movie.addFunction(self.__setState, "Pressed")

            source_push_leave.addTask("TaskMovie2SocketLeave", SocketName="socket", Movie2=MoviePush)
            source_push_leave.addNotify(Notificator.onMovie2ButtonMouseLeave, self.object)
            source_push_leave.addFunction(self.__setState, "Release")

            # source_pressed_click_rel.addTask("TaskMovie2SocketClick", SocketName = "socket",
            #                                  Movie2 = MoviePush, isDown = False, Already = True)
            source_pressed_click_rel.addTask("TaskMovie2SocketClick", SocketName="socket",
                                             Movie2=MoviePush, isDown=False, isPressed=False)
            source_pressed_click_rel.addFunction(self.__setState, "Click")

        source.addDisable(MoviePush)

    def __statePressed(self, source, MoviePressed):
        if MoviePressed is None:
            source.addFunction(self.__setState, "Click")
            return

        source.addScope(self.__scopeEnable, MoviePressed)
        source.addDelay(0.0)
        source.addNotify(Notificator.onMovie2ButtonPressed, self.object)

        with source.addRaceTask(4) as (source_pressed_click_rel, source_pressed_leave, source_block, source_selected):
            source_pressed_click_rel.addTask("TaskMovie2SocketClick", SocketName="socket",
                                             Movie2=MoviePressed, isDown=False, isPressed=False, Already=True)
            source_pressed_click_rel.addFunction(self.__setState, "Click")

            source_pressed_leave.addTask("TaskMovie2SocketLeave", SocketName="socket", Movie2=MoviePressed)
            source_pressed_leave.addNotify(Notificator.onMovie2ButtonMouseLeave, self.object)
            source_pressed_leave.addFunction(self.__setState, "Release")

            source_block.addSemaphore(self.SemaphoreBlock, From=True)
            source_block.addFunction(self.__setState, "BlockEnter")

            source_selected.addSemaphore(self.SemaphoreSelected, From=True)
            source_selected.addFunction(self.__setState, "SelectedEnter")

        source.addDisable(MoviePressed)

    def __stateRelease(self, source, MovieRelease):
        if MovieRelease is None:
            source.addNotify(Notificator.onMovie2ButtonRelease, self.object)
            source.addFunction(self.__setState, "Release_Play")
            return

        source.addScope(self.__scopeEnable, MovieRelease)
        source.addNotify(Notificator.onMovie2ButtonRelease, self.object)
        source.addDelay(0.0)

        with source.addRaceTask(2) as (source_release_movie, source_release_enter):
            source_release_movie.addTask("TaskMouseButtonClick", isDown=False)
            source_release_movie.addFunction(self.__setState, "Release_Play")

            source_release_enter.addTask("TaskMovie2SocketEnter", SocketName="socket", Movie2=MovieRelease)
            source_release_enter.addFunction(self.__setState, "Pressed")

        source.addDisable(MovieRelease)

    def __stateReleasePlay(self, source, MovieRelease):
        if MovieRelease is None:
            source.addFunction(self.__setState, "Idle")
            return

        source.addScope(self.__scopeEnable, MovieRelease)
        source.addTask("TaskMovie2Play", Movie2=MovieRelease)
        source.addTask("TaskMovie2Rewind", Movie2=MovieRelease)
        source.addFunction(self.__setState, "Idle")
        source.addDisable(MovieRelease)

    def __stateClick(self, source, MovieClick):
        if MovieClick is None:
            source.addNotify(Notificator.onButtonClickBegin, self.object)
            source.addNotify(Notificator.onButtonClick, self.object)
            source.addNotify(Notificator.onMovie2ButtonClick, self.object)
            source.addFunction(self.__setState, "Idle")
            source.addNotify(Notificator.onMovie2ButtonClickEnd, self.object)
            return

        source.addScope(self.__scopeEnable, MovieClick)
        source.addNotify(Notificator.onButtonClickBegin, self.object)
        source.addNotify(Notificator.onButtonClick, self.object)
        source.addNotify(Notificator.onMovie2ButtonClick, self.object)
        source.addTask("TaskMovie2Play", Movie2=MovieClick)
        source.addFunction(self.__setState, "Idle")
        source.addNotify(Notificator.onMovie2ButtonClickEnd, self.object)
        source.addDisable(MovieClick)

    def __stateBlockEnter(self, source, MovieBlockEnter):
        if MovieBlockEnter is None:
            source.addFunction(self.__setState, "Block")
            return
        source.addScope(self.__scopeEnable, MovieBlockEnter)
        source.addTask("TaskMovie2Play", Movie2=MovieBlockEnter, Wait=True)
        source.addFunction(self.__setState, "Block")

        source.addDisable(MovieBlockEnter)

    def __stateBlock(self, source, MovieBlock):
        if MovieBlock is None:
            source.addSemaphore(self.SemaphoreBlock, From=False)
            source.addFunction(self.__setState, "BlockEnd")
            return
        source.addScope(self.__scopeEnable, MovieBlock)

        source.addSemaphore(self.SemaphoreBlock, From=False)
        source.addFunction(self.__setState, "BlockEnd")

        source.addDisable(MovieBlock)

    def __stateBlockEnd(self, source, MovieBlockEnd):
        if MovieBlockEnd is None:
            source.addFunction(self.__setState, "Idle")
            return
        source.addScope(self.__scopeEnable, MovieBlockEnd)

        source.addTask("TaskMovie2Play", Movie2=MovieBlockEnd, Wait=True)

        with source.addRaceTask(2) as (source_idle, source_selected):
            source_selected.addSemaphore(self.SemaphoreSelected, From=True)
            source_selected.addFunction(self.__setState, "SelectedEnter")

            source_idle.addSemaphore(self.SemaphoreSelected, From=False)
            source_idle.addFunction(self.__setState, "Idle")

        source.addDisable(MovieBlockEnd)

    def __stateSelectedEnter(self, source, MovieSelectedEnter):
        if MovieSelectedEnter is None:
            source.addFunction(self.__setState, "Selected")
            return
        source.addScope(self.__scopeEnable, MovieSelectedEnter)
        source.addTask("TaskMovie2Play", Movie2=MovieSelectedEnter, Wait=True)
        source.addFunction(self.__setState, "Selected")

        source.addDisable(MovieSelectedEnter)

    def __stateSelected(self, source, MovieSelected):
        if MovieSelected is None:
            source.addSemaphore(self.SemaphoreSelected, From=False)
            source.addFunction(self.__setState, "SelectedEnd")
            return
        source.addScope(self.__scopeEnable, MovieSelected)

        source.addSemaphore(self.SemaphoreSelected, From=False)
        source.addFunction(self.__setState, "SelectedEnd")

        source.addDisable(MovieSelected)

    def __stateSelectedEnd(self, source, MovieSelectedEnd):
        if MovieSelectedEnd is None:
            source.addFunction(self.__setState, "Idle")
            return
        source.addScope(self.__scopeEnable, MovieSelectedEnd)

        source.addTask("TaskMovie2Play", Movie2=MovieSelectedEnd, Wait=True)

        with source.addRaceTask(2) as (source_idle, source_block):
            source_block.addSemaphore(self.SemaphoreBlock, From=True)
            source_block.addFunction(self.__setState, "BlockEnter")

            source_idle.addSemaphore(self.SemaphoreBlock, From=False)
            source_idle.addFunction(self.__setState, "Idle")

        source.addDisable(MovieSelectedEnd)

    def setState(self, state):
        states = ("Idle", "Appear", "Enter", "Leave", "Over", "Click", "Push", "Pressed",
                  "Release", "Block", "BlockEnter", "BlockEnd", "Selected", "SelectedEnter", "SelectedEnd")
        if state not in states:
            return

        self.__setState(state)
        self.custom = True

        self.EventSkipState()

    def scopeDisableAllMovies(self, source):
        for Movie in self.Movies.itervalues():
            if Movie is None:
                continue

            source.addDisable(Movie)

    def getStateMovie(self, state):
        touchpad_ignore = ["Enter", "Over", "Leave", "Release"]
        defaults = {
            "Over": "Idle",
            "Pressed": "Idle",
            "Block": "Idle",
            "Selected": "Idle",
        }
        default_state_name = defaults.get(state)
        movie_default = self.Movies.get(default_state_name)
        movie_state = self.Movies.get(state, movie_default)

        if Mengine.hasTouchpad() is True and state in touchpad_ignore:
            # mobile devices don't have this states - use default or nothing
            return movie_default

        return movie_state

    def _onActivate(self):
        super(Movie2Button, self)._onActivate()

        if self.custom is False:
            self.state = "Appear"

            if "Appear" not in self.Movies:
                self.state = "Idle"

        MovieIdle = self.getStateMovie("Idle")
        MovieAppear = self.getStateMovie("Appear")
        MovieEnter = self.getStateMovie("Enter")
        MovieLeave = self.getStateMovie("Leave")
        MovieOver = self.getStateMovie("Over")
        MovieClick = self.getStateMovie("Click")
        MoviePush = self.getStateMovie("Push")
        MoviePressed = self.getStateMovie("Pressed")
        MovieRelease = self.getStateMovie("Release")
        MovieBlock = self.getStateMovie("Block")
        MovieBlockEnd = self.getStateMovie("BlockEnd")
        MovieBlockEnter = self.getStateMovie("BlockEnter")
        MovieSelected = self.getStateMovie("Selected")
        MovieSelectedEnd = self.getStateMovie("SelectedEnd")
        MovieSelectedEnter = self.getStateMovie("SelectedEnter")

        self.tc = TaskManager.createTaskChain(Repeat=True, NoCheckAntiStackCycle=True)

        with self.tc as source_repeat:
            Scopes = dict(
                Idle=Functor(self.__stateIdle, MovieIdle),
                Enter=Functor(self.__stateEnter, MovieEnter),
                Appear=Functor(self.__stateAppear, MovieAppear),
                Over=Functor(self.__stateOver, MovieOver),
                Leave=Functor(self.__stateLeave, MovieLeave),
                Click=Functor(self.__stateClick, MovieClick),
                Push=Functor(self.__statePush, MoviePush),
                Pressed=Functor(self.__statePressed, MoviePressed),
                Release=Functor(self.__stateRelease, MovieRelease),
                Release_Play=Functor(self.__stateReleasePlay, MovieRelease),
                Block=Functor(self.__stateBlock, MovieBlock),
                BlockEnter=Functor(self.__stateBlockEnter, MovieBlockEnter),
                BlockEnd=Functor(self.__stateBlockEnd, MovieBlockEnd),
                Selected=Functor(self.__stateSelected, MovieSelected),
                SelectedEnter=Functor(self.__stateSelectedEnter, MovieSelectedEnter),
                SelectedEnd=Functor(self.__stateSelectedEnd, MovieSelectedEnd),
            )

            def __states(isSkip, cb):
                cb(isSkip, self.state)

            with source_repeat.addRaceTask(2) as (source_switch, source_skip):
                # source_switch.addFunction(self.__debug_print, 'BEFORE')
                source_switch.addScopeSwitch(Scopes, __states)
                # source_switch.addFunction(self.__debug_print, 'AFTER')

                source_skip.addEvent(self.EventSkipState)
                source_skip.addScope(self.scopeDisableAllMovies)

    def __debug_print(self, v):
        print('TC CURRENT_STATE', v, self.state)

    def _onDeactivate(self):
        super(Movie2Button, self)._onDeactivate()

        if self.tc is not None:
            self.tc.cancel()
            self.tc = None

        for mov in self.Movies.itervalues():
            mov.setEnable(False)