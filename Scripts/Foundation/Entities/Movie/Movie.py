from Foundation.Entity.BaseAnimatable import BaseAnimatable

from Foundation.GroupManager import GroupManager

class Movie(BaseAnimatable):
    @staticmethod
    def declareORM(Type):
        BaseAnimatable.declareORM(Type)

        Type.addAction(Type, "Wait")
        Type.addAction(Type, "ExtraGroupName")
        Type.addAction(Type, "ResourceMovie")
        Type.addAction(Type, "DisableLayers",
                       Update=Movie.__updateDisableLayers,
                       Append=Movie.__appendDisableLayers,
                       Remove=Movie.__removeDisableLayers)
        Type.addAction(Type, "LastFrameSubMovies",
                       Update=Movie.__updateLastFrameSubMovies,
                       Append=Movie.__appendLastFrameSubMovies,
                       Remove=Movie.__removeLastFrameSubMovies)
        pass

    def _onUpdateEnable(self, value):
        self.object.onMovieUpdateEnable(self.object)

    def __init__(self):
        super(Movie, self).__init__()

        self.movie = None
        self.socketParams = None
        pass

    def __updateSpeedFactor(self, value):
        self.movie.setAnimationSpeedFactor(value)
        pass

    def __updateDisableLayers(self, layers):
        for layer in layers:
            self.movie.setEnableMovieLayers(layer, False)
            pass
        pass

    def __appendDisableLayers(self, index, layer):
        self.movie.setEnableMovieLayers(layer, False)
        pass

    def __removeDisableLayers(self, index, layer, old):
        self.movie.setEnableMovieLayers(layer, True)
        pass

    def __updateLastFrameSubMovies(self, submovies):
        for submovie_name in submovies:
            submovie = self.getSubMovie(submovie_name)
            submovie.setLastFrame()
            pass
        pass

    def __appendLastFrameSubMovies(self, index, submovie_name):
        submovie = self.getSubMovie(submovie_name)
        Animation = submovie.getAnimation()
        Animation.setLastFrame()
        pass

    def __removeLastFrameSubMovies(self, index, submovie_name, old):
        submovie = self.getSubMovie(submovie_name)
        Animation = submovie.getAnimation()
        Animation.setLastFrame()
        pass

    def getDuration(self):
        return self.movie.getDuration()
        pass

    def getAnimatable(self):
        return self.movie
        pass

    def getMovie(self):
        return self.movie
        pass

    def getSocket(self, name):
        socket = self.movie.getSocket(name)

        return socket
        pass

    def hasSocket(self, name):
        return self.movie.hasSocket(name)
        pass

    def isSocketMouseEnter(self, name):
        # fix for HotSpot isMousePickerOver Error
        if self.isActivate() is False:
            return False

        socket = self.getSocket(name)

        if socket is None:
            return False
            pass

        over = socket.isMousePickerOver()

        return over
        pass

    def isAnySocketMouseEnter(self):
        sockets = self.movie.getSockets()

        for movie, name, hotspot in sockets:
            over = hotspot.isMousePickerOver()

            if over is True:
                return True
                pass
            pass

        return False
        pass

    def getMovieSlot(self, name):
        slot = self.movie.getMovieSlot(name)

        return slot
        pass

    def removeAllMovieSlotNode(self, name):
        successful = self.movie.removeAllMovieSlotNode(name)

        return successful
        pass

    def getWorldAnchorPoint(self):
        WAP = self.movie.getWorldAnchorPoint()

        return WAP
        pass

    def getMovieSlotOffsetPosition(self, name):
        WAP = self.movie.getWorldAnchorPoint()

        slot = self.movie.getMovieSlot(name)
        SWP = slot.getWorldPosition()

        return SWP - WAP
        pass

    def getMovieSlotWorldPosition(self, name):
        slot = self.movie.getMovieSlot(name)

        WP = slot.getWorldPosition()

        return WP
        pass

    def hasMovieSlot(self, name):
        result = self.movie.hasMovieSlot(name)

        return result
        pass

    def getMovieText(self, name):
        text = self.movie.getMovieText(name)

        return text
        pass

    def hasMovieText(self, name):
        result = self.movie.hasMovieText(name)

        return result
        pass

    def setMovieEvent(self, name, cb):
        result = self.movie.setMovieEvent(name, cb)

        return result
        pass

    def hasMovieEvent(self, name):
        result = self.movie.hasMovieEvent(name)

        return result
        pass

    def filterLayers(self, type):
        result = self.movie.filterLayers(type)

        return result
        pass

    def getSubMovie(self, name):
        submovie = self.movie.getSubMovie(name)

        return submovie
        pass

    def hasSubMovie(self, name):
        result = self.movie.hasSubMovie(name)

        return result
        pass

    def _onInitialize(self, obj):
        super(Movie, self)._onInitialize(obj)

        self.movie = self.createChild("Movie")

        name = self.getName()
        self.movie.setName(name)

        self.movie.setResourceMovie(self.ResourceMovie)

        self.movie.setEventListener(onMovieGetInternal=self.__onMovieGetInternal,
                                    onMovieActivateInternal=self.__onMovieActivateInternal,
                                    onMovieDeactivateInternal=self.__onMovieDeactivateInternal,
                                    onAnimatableEnd=self.__onAnimatableEnd,
                                    onAnimatableStop=self.__onAnimatableStop)

        sockets = self.movie.getSockets()

        for movie, name, hotspot in sockets:
            hotspot.setEventListener(onHandleMouseEnter=Functor(self.__onHandleMouseEnter, name, hotspot),
                                     onHandleMouseLeave=Functor(self.__onHandleMouseLeave, name, hotspot),
                                     onHandleMouseButtonEvent=Functor(self.__onHandleMouseButtonEvent, name, hotspot),
                                     onHandleMouseMove=Functor(self.__onHandleMouseMove, name, hotspot))
            pass

        self.movie.enable()
        pass

    def _onFinalize(self):
        super(Movie, self)._onFinalize()

        sockets = self.movie.getSockets()

        for movie, name, hotspot in sockets:
            eventation = hotspot.getEventation()
            eventation.removeEvents()
            pass

        Mengine.destroyNode(self.movie)
        self.movie = None
        pass

    def setSocketHandle(self, name, type, value):
        if self.socketParams is None:
            self.socketParams = {}
            pass

        if name not in self.socketParams:
            self.socketParams[name] = {}
            pass

        socketParam = self.socketParams[name]
        socketParam[type] = value
        pass

    def __onHandleMouseEnter(self, x, y, name, hotspot):
        if self.object is not None:
            self.object.onMovieSocketEnterEvent(self.object, name, hotspot, x, y)
            pass

        if self.socketParams is None:
            return True
            pass

        socketParam = self.socketParams.get(name, {})
        handler = socketParam.get("enter", True)

        return handler
        pass

    def __onHandleMouseLeave(self, name, hotspot):
        if self.object is not None:
            self.object.onMovieSocketLeaveEvent(self.object, name, hotspot)
            pass
        pass

    def __onHandleMouseButtonEvent(self, touchId, x, y, button, pressure, isDown, isPressed, name, hotspot):
        if self.object is not None:
            self.object.onMovieSocketButtonEvent(self.object, name, hotspot, touchId, x, y, button, isDown, isPressed)
            pass

        if self.socketParams is None:
            return True
            pass

        socketParam = self.socketParams.get(name, {})
        handler = socketParam.get("button", True)

        return handler
        pass

    def __onHandleMouseMove(self, touchId, x, y, dx, dy, pressure, name, hotspot):
        if self.object is not None:
            self.object.onMovieSocketMoveEvent(self.object, name, hotspot, touchId, x, y, dx, dy)
            pass

        if self.socketParams is None:
            return True
            pass

        socketParam = self.socketParams.get(name, {})
        handler = socketParam.get("move", True)

        return handler
        pass

    def __onMovieGetInternal(self, groupName, name):
        obj = self._findMovieObject(groupName, name)

        return obj
        pass

    def __onMovieDeactivateInternal(self, internalObject):
        if internalObject is None:
            return
            pass

        internalObject.returnToParent()
        pass

    def __onMovieActivateInternal(self, internalObject):
        if internalObject is None:
            return None
            pass

        entityNode = internalObject.getEntityNode()

        return entityNode
        pass

    def _onPreparation(self):
        super(Movie, self)._onPreparation()
        pass

    def _onActivate(self):
        super(Movie, self)._onActivate()
        pass

    def _onDeactivate(self):
        super(Movie, self)._onDeactivate()
        pass

    def _findMovieObject(self, groupName, name):
        group = GroupManager.getGroup(groupName)
        obj = group.getObject(name)

        return obj
        pass

    def _onPlay(self):
        animation = self.movie.getAnimation()

        if self.StartTiming is not None:
            duration = self.ResourceMovie.getDuration()
            frame_duration = self.ResourceMovie.getFrameDuration()

            duration_max = duration - 1.51 * frame_duration

            if self.StartTiming > duration_max:
                animation.setTime(duration_max)
                pass
            else:
                animation.setTime(self.StartTiming)
                pass

            pass

        else:
            animation.setFirstFrame()
            pass
        pass

    def __onAnimatableEnd(self, id):
        if self.validPlayId(id) is False:
            return
            pass

        self.end()
        pass

    def __onAnimatableStop(self, id):
        if self.validPlayId(id) is False:
            return
            pass

        self.end()
        pass

    def getSlots(self):
        slots = self.movie.getSlots()

        return slots
        pass

    def hasMovieNode(self, name):
        result = self.movie.hasMovieNode(name)

        return result
        pass

    def getMovieNode(self, name):
        node = self.movie.getMovieNode(name)

        return node
        pass

    def filterLayers(self, type):
        nodies = self.movie.filterLayers(type)

        return nodies
        pass
    pass