from ObjectAnimatable import ObjectAnimatable

class ObjectMovie2(ObjectAnimatable):
    @staticmethod
    def declareORM(Type):
        ObjectAnimatable.declareORM(Type)

        Type.declareResource("ResourceMovie")
        Type.declareParam("CompositionName")
        Type.declareParam("DisableLayers")
        Type.declareParam("DisableSubMovies")
        Type.declareParam("SpeedFactor")
        Type.declareParam("TextAliasEnvironment")
        Type.declareParam("LastFrameSubMovies")
        Type.declareParam("ExtraOpacityLayers")
        pass

    def __init__(self):
        super(ObjectMovie2, self).__init__()

        self.onMovieSocketEnterEvent = Event("onMovieSocketEnter")
        self.onMovieSocketLeaveEvent = Event("onMovieSocketLeave")
        self.onMovieSocketButtonEvent = Event("onMovieSocketButton")
        self.onMovieSocketMoveEvent = Event("onMovieSocketMove")
        self.onMovieUpdateEnable = Event("onMovieUpdateEnable")

        self.StartProportion = None
        pass

    def _onParams(self, params):
        super(ObjectMovie2, self)._onParams(params)

        self.initResource("ResourceMovie", params)
        self.initParam("CompositionName", params, None)
        self.initParam("DisableLayers", params, [])
        self.initParam("DisableSubMovies", params, [])
        self.initParam("SpeedFactor", params, 1.0)
        self.initParam("TextAliasEnvironment", params, "")
        self.initParam("LastFrameSubMovies", params, [])
        self.initParam("ExtraOpacityLayers", params, {})  # contain pairs of layer additional alpha multiplier
        pass

    def getCompositionBounds(self):
        return self.getEntity().getCompositionBounds()

    def hasCompositionBounds(self):
        return self.getEntity().hasCompositionBounds()

    def getMovieSlot(self, SlotName):
        if self.isActive() is False:
            Trace.log('Object', 0, 'Movie2 %s is not active' % self.getName())
            return None

        Entity = self.getEntity()

        Slot = Entity.getMovieSlot(SlotName)

        return Slot

    def getMovieText(self, name):
        if self.isActive() is False:
            Trace.log("Object", 0, "Movie '%s' is not active" % self.getName())
            return

        text = self.entity.getMovieText(name)
        return text

    def hasMovieText(self, name):
        if self.isActive() is False:
            Trace.log("Object", 0, "Movie '%s' is not active" % self.getName())
            return

        result = self.entity.hasMovieText(name)
        return result

    def getSocket(self, SocketName):
        if self.isActive() is False:
            Trace.log('Object', 0, 'Movie2 %s is not active' % self.getName())
            return None

        Entity = self.getEntity()

        Socket = Entity.getSocket(SocketName)

        return Socket

    def getSockets(self):
        """ :returns: list of tuples with movie, name, hotspot inside """
        Entity = self.getEntity()
        Sockets = Entity.getSockets()

        return Sockets

    def getSlots(self):
        if self.isActive() is False:
            return False

        MovieEntity = self.getEntity()
        slots = MovieEntity.getSlots()
        return slots

    def hasMovieSlot(self, SlotName):
        return self.hasSlot(SlotName)

    def hasSlot(self, SlotName):
        if self.isActive() is False:
            return False

        MovieEntity = self.getEntity()

        return MovieEntity.hasMovieSlot(SlotName)

    def hasSocket(self, SlotName):
        if self.isActive() is False:
            return False

        MovieEntity = self.getEntity()

        return MovieEntity.hasSocket(SlotName)

    def getDuration(self):
        ResourceMovie = self.getResourceMovie()

        duration = ResourceMovie.getCompositionDuration(self.getCompositionName())

        return duration

    def getFrameDuration(self):
        ResourceMovie = self.getResourceMovie()

        frameDuration = ResourceMovie.getCompositionFrameDuration(self.getCompositionName())

        return frameDuration

    def getLastFrameTiming(self):
        ResourceMovie = self.getResourceMovie()

        duration = ResourceMovie.getCompositionDuration(self.getCompositionName())
        frameDuration = ResourceMovie.getCompositionFrameDuration(self.getCompositionName())

        lastFrameTiming = duration - frameDuration

        return lastFrameTiming

    def setTimingProportion(self, proportion):
        if self.isActive() is False:
            return

        MovieEntity = self.getEntity()

        animation = MovieEntity.movie.getAnimation()
        Duration = self.getDuration()
        Time = Duration * proportion

        animation.setTime(Time)
        pass

    def getTimingProportion(self):
        if self.isActive() is False:
            return 0.0

        MovieEntity = self.getEntity()

        Duration = self.getDuration()

        animation = MovieEntity.movie.getAnimation()
        Time = animation.getTime()
        # print 'Duration', Duration, Time
        Proportion = Time / Duration

        return Proportion
        pass

    def getTimeFromProportion(self, proportion):
        if self.isActive() is False:
            return 0.0

        Duration = self.getDuration()

        Time = Duration * proportion

        return Time

    def setupMovieTextArguments(self, TextName, *Args):
        if self.isActive() is False:
            return False

        Entity = self.getEntity()

        Text = Entity.getMovieText(TextName)

        if Text is None:
            return False
            pass

        Text.setTextFormatArgs(*Args)

        return True

    def setupMovieTextColor(self, TextName, Color):
        if len(Color) != 4:
            Trace.log("Object", 0, "setupMovieTextColor - color should contain 4 float values from 0 to 1 (not {!r})".format(Color))
            return False

        if self.isActive() is False:
            return False

        Entity = self.getEntity()

        Text = Entity.getMovieText(TextName)

        if Text is None:
            return False

        Text.setFontColor(Color)

        return True

    def setupMovieTextFont(self, TextName, Font):
        if Mengine.hasFont(Font) is False:
            Trace.log("Object", 0, "setupMovieTextColor - font {!r} is not found!".format(Font))
            return False

        if self.isActive() is False:
            return False

        Entity = self.getEntity()

        Text = Entity.getMovieText(TextName)

        if Text is None:
            return False

        Text.setFontName(Font)

        return True

    def getMovie(self):
        if self.isActive() is False:
            return None
            pass

        MovieEntity = self.getEntity()

        movie = MovieEntity.getMovie()

        return movie
        pass
    pass

    def setLayerExtraOpacity(self, layer, opacity):
        self.insertDictParam("ExtraOpacityLayers", layer, opacity)

    def resetLayerExtraOpacity(self, layer):
        self.popDictParam("ExtraOpacityLayers", layer)

    def setMultipleLayersExtraOpacity(self, layers, opacity):
        for layer in layers:
            self.setLayerExtraOpacity(layer, opacity)

    def resetMultipleLayersExtraOpacity(self, layers):
        for layer in layers:
            self.resetLayerExtraOpacity(layer)

    def getFirstSocketTuple(self):
        if not self.isActive():
            return

        sockets = self.entity.movie.getSockets()
        if len(sockets) > 0:
            return sockets[0]