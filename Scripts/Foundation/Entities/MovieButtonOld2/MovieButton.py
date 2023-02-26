from Foundation.Entity.BaseEntity import BaseEntity

from MovieButtonStateClick import MovieButtonStateClick
from MovieButtonStateEnter import MovieButtonStateEnter
from MovieButtonStateIdle import MovieButtonStateIdle
from MovieButtonStateLeave import MovieButtonStateLeave
from MovieButtonStateOver import MovieButtonStateOver

class MovieButton(BaseEntity):
    @staticmethod
    def declareORM(Type):
        BaseEntity.declareORM(Type)
        Type.addAction(Type, "ResourceMovieIdle")
        Type.addAction(Type, "ResourceMovieEnter")
        Type.addAction(Type, "ResourceMovieOver")
        Type.addAction(Type, "ResourceMovieClick")
        Type.addAction(Type, "ResourceMoviePressed")
        Type.addAction(Type, "ResourceMovieLeave")
        Type.addAction(Type, "ResourceMovieRelease")
        Type.addAction(Type, "ResourceMoviePush")

        Type.addAction(Type, "KeyTag")
        Type.addAction(Type, "BlockKeys")
        Type.addAction(Type, "Block")
        Type.addAction(Type, "TextFont")
        Type.addAction(Type, "TextAlign")
        Type.addAction(Type, "TextVerticalAlign")
        Type.addAction(Type, "TextArgs", Update=MovieButton.__updateTextArgs)
        pass

    def __updateTextArgs(self, args):
        text_field = None

        if self.currentState is None:
            returnSwapSwa
            pass

        currentMovie = self.currentState.getMovie()
        if currentMovie is None:
            return
            pass

        list = currentMovie.filterLayers("MovieText")

        if len(list) == 0:
            list = currentMovie.filterLayers("MovieTextCenter")
            pass

        if len(list) == 0 and args is not None:
            Trace.log("Entity", 0, "MovieButton %s in group %s invalid set TextArgs, not found slot text in aep composition" % (self.object.name, self.object.getGroupName()))
            return
            pass

        if len(list) == 0:
            return
            pass

        data = list[0]
        movie, text_field = data

        if self.TextFont is not None:
            text_field.setFontName(self.TextFont)
            pass

        if self.TextAlign is None:
            pass
        elif self.TextAlign == "Left":
            text_field.setLeftAlign()
            pass
        elif self.TextAlign == "Center":
            text_field.setCenterAlign()
            pass
        elif self.TextAlign == "Right":
            text_field.setRightAlign()
            pass
        else:
            Trace.log("Entity", 0, "MovieButton '%s:%s' invalid TextAlign '%s'" % (self.object.name, self.object.getGroupName(), self.TextAlign))
            pass

        if self.TextVerticalAlign is None:
            pass
        elif self.TextVerticalAlign == "Bottom":
            text_field.setVerticalBottomAlign()
            pass
        elif self.TextVerticalAlign == "Center":
            text_field.setVerticalCenterAlign()
            pass
        elif self.TextVerticalAlign == "Top":
            text_field.setVerticalTopAlign()
            pass
        else:
            Trace.log("Entity", 0, "MovieButton '%s:%s' invalid TextVerticalAlign '%s'" % (self.object.name, self.object.getGroupName(), self.TextVerticalAlign))
            pass

        if args is None:
            text_field.removeTextFormatArgs()
            return
            pass

        if isinstance(args, tuple) is True:
            text_field.setTextFormatArgs(*args)
        else:
            text_field.setTextFormatArgs(args)
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
        self.onKeyEventObserver = None
        self.Clickable = None
        self.currentState = None
        self.StateIdle = None
        self.StateEnter = None
        self.StateLeave = None
        self.nextState = None
        self.changed = False
        pass

    def _updateInteractive(self, value):
        super(MovieButton, self)._updateInteractive(value)

        self.setClickable(value)
        if value is True:
            if self.currentState is not None:
                self.currentState.updateClickable()
                pass
            pass
        pass

    def setClickable(self, value):
        self.Clickable = value
        pass

    def changeState(self, newStateName):
        if newStateName == "Idle":
            newState = self.StateIdle
            pass
        elif newStateName == "Enter":
            newState = self.StateEnter
            pass
        elif newStateName == "Leave":
            newState = self.StateLeave
            pass
        elif newStateName == "Over":
            newState = self.StateOver
            pass
        elif newStateName == "Click":
            newState = self.StateClick
            pass
        else:
            Trace.log("Entity", 0, "changeState %s %s %s" % (self.object.name, self.currentState, newStateName))
            return
            pass

        self.nextState = newState

        if self.changed is True:
            return
            pass

        self.checkStates()
        pass

    def checkStates(self):
        self.changed = True

        state = self.nextState
        self.nextState = None

        state.enable()

        if self.currentState is not None and self.currentState != state:
            self.currentState.deactivate()
            pass

        state.activate()

        self.currentState = state
        self.changed = False

        self.__updateTextArgs(self.TextArgs)

        self.onChangeState()
        pass

    def onChangeState(self):
        if self.nextState is not None:
            self.checkStates()
            pass
        pass

    def _onInitialize(self, obj):
        super(MovieButton, self)._onInitialize(obj)
        if self.ResourceMovieIdle is None:
            Trace.log("Entity", 0, "MovieButton _onInitialize failed, ResourceMovieIdle is None")
            return
            pass

        self.StateIdle = MovieButtonStateIdle()
        self.StateIdle.onParams(self, self.ResourceMovieIdle)

        if self.ResourceMovieEnter is not None:
            self.StateEnter = MovieButtonStateEnter()
            self.StateEnter.onParams(self, self.ResourceMovieEnter)
            pass

        if self.ResourceMovieLeave is not None:
            self.StateLeave = MovieButtonStateLeave()
            self.StateLeave.onParams(self, self.ResourceMovieLeave)
            pass

        if self.ResourceMovieOver is None:
            Trace.log("Entity", 0, "MovieButton _onInitialize failed, MovieButtonStateOver is None")
            return
            pass

        self.StateOver = MovieButtonStateOver()
        self.StateOver.onParams(self, self.ResourceMovieOver)

        if self.ResourceMovieClick is None:
            Trace.log("Entity", 0, "MovieButton _onInitialize failed, ResourceMovieClick is None")
            return
            pass
        self.StateClick = MovieButtonStateClick()
        self.StateClick.onParams(self, self.ResourceMovieClick)
        pass

    def __disableAll(self):
        if self.StateIdle is not None:
            self.StateIdle.disable()
            pass
        if self.StateEnter is not None:
            self.StateEnter.disable()
            pass
        if self.StateLeave is not None:
            self.StateLeave.disable()
            pass
        if self.StateOver is not None:
            self.StateOver.disable()
            pass
        if self.StateClick is not None:
            self.StateClick.disable()
            pass
        pass

    def _onPreparation(self):
        super(MovieButton, self)._onPreparation()
        self.__disableAll()
        pass

    def _onActivate(self):
        super(MovieButton, self)._onActivate()
        self.changeState("Idle")
        pass

    def _onDeactivate(self):
        super(MovieButton, self)._onDeactivate()
        pass

    def _onFinalize(self):
        super(MovieButton, self)._onFinalize()

        self.__disableAll()
        pass
    pass