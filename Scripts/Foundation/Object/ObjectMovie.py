from ObjectAnimatable import ObjectAnimatable

class ObjectMovie(ObjectAnimatable):
    @staticmethod
    def declareORM(Type):
        ObjectAnimatable.declareORM(Type)

        Type.addResource(Type, "ResourceMovie")

        Type.addParam(Type, "ExtraGroupName")
        Type.addParam(Type, "SpeedFactor")
        Type.addParam(Type, "DisableLayers")
        pass

    def __init__(self):
        super(ObjectMovie, self).__init__()

        self.onMovieSocketEnterEvent = Event("onMovieSocketEnter")
        self.onMovieSocketLeaveEvent = Event("onMovieSocketLeave")
        self.onMovieSocketButtonEvent = Event("onMovieSocketButton")
        self.onMovieSocketMoveEvent = Event("onMovieSocketMove")
        self.onMovieUpdateEnable = Event("onMovieUpdateEnable")
        pass

    def _onParams(self, params):
        super(ObjectMovie, self)._onParams(params)

        self.initResource("ResourceMovie", params)

        self.initParam("ExtraGroupName", params, None)
        self.initParam("SpeedFactor", params, 1.0)
        self.initParam("DisableLayers", params, [])
        self.initParam("LastFrameSubMovies", params, [])
        pass

    def getArrowPoint(self):
        return (0, 0)
        pass

    def getDuration(self):
        ResourceMovie = self.getResourceMovie()

        duration = ResourceMovie.getDuration()

        return duration
        pass

    def getFrameDuration(self):
        ResourceMovie = self.getResourceMovie()

        duration = ResourceMovie.getFrameDuration()

        return duration
        pass

    def getLastFrameTiming(self):
        ResourceMovie = self.getResourceMovie()

        duration = ResourceMovie.getDuration()
        frameDuration = ResourceMovie.getFrameDuration()

        lastFrameTiming = duration - frameDuration

        return lastFrameTiming
        pass

    def getMovieSlot(self, SlotName):
        if self.isActive() is False:
            Trace.log('Object', 0, 'Movie %s is not active' % self.getName())
            return None
            pass

        Entity = self.getEntity()

        Slot = Entity.getMovieSlot(SlotName)

        return Slot

    def getMovieText(self, name):
        if self.isActive() is False:
            Trace.log("Object", 0, "Movie '%s' is not active" % self.getName())
            return

        text = self.entity.getMovieText(name)
        return text

    def getSocket(self, SocketName):
        if self.isActive() is False:
            Trace.log('Object', 0, 'Movie %s is not active' % self.getName())
            return None
            pass

        Entity = self.getEntity()

        Socket = Entity.getSocket(SocketName)

        return Socket
        pass

    def attachMovieSlotNode(self, SlotName, Node):
        if self.isActive() is False:
            return False
            pass

        Entity = self.getEntity()

        Slot = Entity.getMovieSlot(SlotName)

        if Slot is None:
            return False
            pass

        Slot.addChild(Node)

        return True
        pass

    def destroyAllMovieSlotNode(self, SlotName):
        if self.isActive() is False:
            return False
            pass

        Entity = self.getEntity()

        Slot = Entity.getMovieSlot(SlotName)

        if Slot is None:
            return False
            pass

        Slot.destroyChildren()

        return True
        pass

    def removeAllMovieSlotNode(self, SlotName):
        if self.isActive() is False:
            return False
            pass

        Entity = self.getEntity()

        successful = Entity.removeAllMovieSlotNode(SlotName)

        return successful
        pass

    def getAllMovieSlotNode(self, SlotName):
        if self.isActive() is False:
            return None
            pass

        Entity = self.getEntity()

        Slot = Entity.getMovieSlot(SlotName)

        if Slot is None:
            return None
            pass

        children = Slot.getAllChildren()

        return children
        pass

    def attachMovieSlotObject(self, SlotName, Object):
        if Object.isActive() is False:
            return False
            pass

        ObjectEntityNode = Object.getEntityNode()

        return self.attachMovieSlotNode(SlotName, ObjectEntityNode)
        pass

    def setupMovieTextArguments(self, TextName, *Args):
        if self.isActive() is False:
            return False
            pass

        Entity = self.getEntity()

        Text = Entity.getMovieText(TextName)

        if Text is None:
            return False
            pass

        Text.setTextFormatArgs(*Args)

        return True
        pass

    def getMovieSlotOffsetPosition(self, SlotName):
        if self.isActive() is False:
            return None
            pass

        MovieEntity = self.getEntity()

        if MovieEntity.hasMovieSlot(SlotName) is False:
            return None
            pass

        WP = MovieEntity.getMovieSlotOffsetPosition(SlotName)

        return WP
        pass

    def getMovieSlotWorldPosition(self, SlotName):
        if self.isActive() is False:
            return None
            pass

        MovieEntity = self.getEntity()

        if MovieEntity.hasMovieSlot(SlotName) is False:
            return None
            pass

        WP = MovieEntity.getMovieSlotWorldPosition(SlotName)

        return WP
        pass

    def hasSlot(self, SlotName):
        if self.isActive() is False:
            return False
            pass

        MovieEntity = self.getEntity()

        return MovieEntity.hasMovieSlot(SlotName)
        pass

    def hasSocket(self, SlotName):
        if self.isActive() is False:
            return False
            pass

        MovieEntity = self.getEntity()

        return MovieEntity.hasSocket(SlotName)
        pass

    def enableSocket(self, SocketName, Enable=True):
        if self.isActive() is False:
            return False
            pass

        MovieEntity = self.getEntity()

        if MovieEntity.hasSocket(SocketName) is False:
            return False
            pass

        socket = MovieEntity.getSocket(SocketName)

        if Enable is True:
            socket.enable()
            pass
        else:
            socket.disable()
            pass

        return True
        pass

    def hasMovieNode(self, name):
        if self.isActive() is False:
            return False
            pass

        MovieEntity = self.getEntity()

        result = MovieEntity.hasMovieNode(name)

        return result
        pass

    def getMovie(self):
        if self.isActive() is False:
            return None
            pass

        MovieEntity = self.getEntity()

        movie = MovieEntity.getMovie()

        return movie
        pass

    def getMovieNode(self, name):
        if self.isActive() is False:
            return None
            pass

        MovieEntity = self.getEntity()

        node = MovieEntity.getMovieNode(name)

        return node
        pass

    def getMovieNodies(self, type):
        if self.isActive() is False:
            return []
            pass

        MovieEntity = self.getEntity()

        nodies = MovieEntity.filterLayers(type)

        return nodies
        pass

    def setTimingProportion(self, proportion):
        if self.isActive() is False:
            return
            pass

        MovieEntity = self.getEntity()

        Duration = MovieEntity.movie.getDuration()

        animation = MovieEntity.movie.getAnimation()
        animation.setTime(Duration * proportion)
        pass

    def getTimingProportion(self):
        if self.isActive() is False:
            return
            pass

        MovieEntity = self.getEntity()

        Duration = MovieEntity.movie.getDuration()
        Timing = MovieEntity.movie.getTiming()
        return Timing / Duration
        pass