from Foundation.Entity.BaseAnimatable import BaseAnimatable

class Movie2(BaseAnimatable):
    @staticmethod
    def declareORM(Type):
        BaseAnimatable.declareORM(Type)
        Type.addAction(Type, "ResourceMovie")
        Type.addAction(Type, "CompositionName")
        Type.addActionActivate(Type, "DisableLayers",
                               Update=Movie2.__updateDisableLayers,
                               Append=Movie2.__appendDisableLayers,
                               Remove=Movie2.__removeDisableLayers)
        Type.addActionActivate(Type, "DisableSubMovies",
                               Update=Movie2.__updateDisableSubMovies,
                               Append=Movie2.__appendDisableSubMovies,
                               Remove=Movie2.__removDisableSubMovies)
        Type.addActionActivate(Type, "TextAliasEnvironment",
                               Update=Movie2.__updateTextAliasEnvironment)
        Type.addAction(Type, "LastFrameSubMovies",
                       Update=Movie2.__updateLastFrameSubMovies,
                       Append=Movie2.__appendLastFrameSubMovies,
                       Remove=Movie2.__removeLastFrameSubMovies)
        Type.addActionActivate(Type, "ExtraOpacityLayers",
                               Update=Movie2.__updateExtraOpacityLayers,
                               InsertDict=Movie2.__insertExtraOpacityLayers,
                               PopDict=Movie2.__popExtraOpacityLayers)
        pass

    def _onUpdateEnable(self, value):
        self.object.onMovieUpdateEnable(self.object)

    def __init__(self):
        super(Movie2, self).__init__()

        self.movie = None
        self.socketParams = None
        pass

    def getCompositionBounds(self):
        return self.movie.getCompositionBounds()

    def hasCompositionBounds(self):
        return self.movie.hasCompositionBounds()

    def getDuration(self):
        animation = self.movie.getAnimation()
        return animation.getDuration()
        pass

    def getAnimatable(self):
        return self.movie
        pass

    def getMovie(self):
        return self.movie
        pass

    def getResourceMovie(self):
        return self.ResourceMovie
        pass

    def _onInitialize(self, obj):
        super(Movie2, self)._onInitialize(obj)

        movie = self.createChild("Movie2")

        name = self.getName()
        movie.setName(name)

        movie.setResourceMovie2(self.ResourceMovie)
        movie.setCompositionName(self.CompositionName)

        movie.setEventListener(onAnimatableEnd=self.__onAnimatableEnd,
                               onAnimatableStop=self.__onAnimatableStop)
        movie.enable()

        sockets = movie.getSockets()
        for movie, name, hotspot in sockets:
            hotspot.setEventListener(onHandleMouseEnter=Functor(self.__onHandleMouseEnter, name, hotspot),
                                     onHandleMouseLeave=Functor(self.__onHandleMouseLeave, name, hotspot),
                                     onHandleMouseButtonEvent=Functor(self.__onHandleMouseButtonEvent, name, hotspot),
                                     onHandleMouseMove=Functor(self.__onHandleMouseMove, name, hotspot))

        self.movie = movie
        pass

    def _onFinalize(self):
        super(Movie2, self)._onFinalize()

        sockets = self.movie.getSockets()
        for movie, name, hotspot in sockets:
            eventation = hotspot.getEventation()
            eventation.removeEvents()
            pass

        eventation = self.movie.getEventation()
        eventation.removeEvents()

        Mengine.destroyNode(self.movie)
        self.movie = None
        pass

    def _updateInteractive(self, value):
        BlockInteractive = self.object.getParam("BlockInteractive")

        if BlockInteractive is True:
            return
            pass

        sockets = self.movie.getSockets()

        for movie, name, hotspot in sockets:
            if value is True:
                hotspot.enable()
                pass
            else:
                hotspot.disable()
                pass
            pass
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

    def __checkSubMovie(self, submovie_name):
        if self.hasSubMovie(submovie_name) is False:
            Trace.log("Movie2", 0, "Movie2.__updateDisableSubMovies: Movie2 '{}' has no submovie '{}'".format(
                self.getName(), submovie_name))
            return False

        return True

    def __updateDisableSubMovies(self, submovies):
        for submovie_name in submovies:
            if self.__checkSubMovie(submovie_name) is False:
                continue

            submovie = self.getSubMovie(submovie_name)
            submovie.setEnable(False)
            pass
        pass

    def __appendDisableSubMovies(self, index, submovie_name):
        if self.__checkSubMovie(submovie_name) is False:
            return

        submovie = self.getSubMovie(submovie_name)
        submovie.setEnable(False)
        pass

    def __removDisableSubMovies(self, index, submovie_name, old):
        if self.__checkSubMovie(submovie_name) is False:
            return

        submovie = self.getSubMovie(submovie_name)
        submovie.setEnable(True)
        pass

    def __updateLastFrameSubMovies(self, submovies):
        for submovie_name in submovies:
            if self.__checkSubMovie(submovie_name) is False:
                continue

            submovie = self.getSubMovie(submovie_name)

            Animation = submovie.getAnimation()
            Animation.setLastFrame()
            pass
        pass

    def __appendLastFrameSubMovies(self, index, submovie_name):
        if self.__checkSubMovie(submovie_name) is False:
            return

        submovie = self.getSubMovie(submovie_name)

        Animation = submovie.getAnimation()
        Animation.setLastFrame()
        pass

    def __removeLastFrameSubMovies(self, index, submovie_name, old):
        if self.__checkSubMovie(submovie_name) is False:
            return

        submovie = self.getSubMovie(submovie_name)

        Animation = submovie.getAnimation()
        Animation.setFirstFrame()
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

    def _onPlay(self):
        animation = self.movie.getAnimation()

        if self.StartTiming is not None:
            duration = self.ResourceMovie.getCompositionDuration(self.CompositionName)
            frame_duration = self.ResourceMovie.getCompositionFrameDuration(self.CompositionName)

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

    def getMovieText(self, name):
        text = self.movie.findText(name)

        return text
        pass

    def hasMovieText(self, name):
        result = self.movie.hasText(name)

        return result
        pass

    def getSocket(self, name):
        socket = self.movie.findSocket(name)

        return socket

    def getMovieSlot(self, name):
        if _DEVELOPMENT is True:
            if self.movie.hasSlot(name) is False:
                Trace.log("Movie2", 0, "Movie2 '{}' hasn't slot '{}'".format(self.getName(), name))
                return

        slot = self.movie.findSlot(name)
        return slot

    def hasMovieSlot(self, name):
        result = self.movie.hasSlot(name)

        return result
        pass

    def getSlots(self):
        slots = self.movie.getSlots()
        return slots

    def getSockets(self):
        """ :returns: list of tuples with movie, name, hotspot inside """
        sockets = self.movie.getSockets()
        return sockets

    def hasSocket(self, name):
        return self.movie.hasSocket(name)
        pass

    def getSubMovie(self, name):
        submovie = self.movie.getSubComposition(name)

        return submovie
        pass

    def hasSubMovie(self, name):
        result = self.movie.hasSubComposition(name)

        return result
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

    def __updateDisableLayers(self, layers):
        for layer in layers:
            self.movie.setEnableMovieLayers(layer, False)

        for (self_movie_ref, socket_name, socket) in self.movie.getSockets():
            if socket_name in layers:
                if socket.isEnable():
                    socket.disable()

    def __appendDisableLayers(self, index, layer):
        self.movie.setEnableMovieLayers(layer, False)
        pass

    def __removeDisableLayers(self, index, layer, old):
        self.movie.setEnableMovieLayers(layer, True)
        pass

    def __insertExtraOpacityLayers(self, layer, opacity):
        self.movie.setExtraOpacityMovieLayers(layer, opacity)

    def __popExtraOpacityLayers(self, layer, opacity):
        self.movie.setExtraOpacityMovieLayers(layer, 1.0)

    def __updateExtraOpacityLayers(self, layer_opacity_dict):
        for layer, opacity in layer_opacity_dict.iteritems():
            self.movie.setExtraOpacityMovieLayers(layer, opacity)

    def __updateTextAliasEnvironment(self, value):
        if value is not None:
            self.movie.setTextAliasEnvironment(str(value))

    def _onPreparation(self):
        super(Movie2, self)._onPreparation()