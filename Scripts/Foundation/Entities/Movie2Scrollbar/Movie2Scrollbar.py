from Foundation.Entity.BaseEntity import BaseEntity
from Foundation.ObjectManager import ObjectManager
from Foundation.TaskManager import TaskManager

class Movie2Scrollbar(BaseEntity):
    @staticmethod
    def declareORM(Type):
        BaseEntity.declareORM(Type)
        Type.addAction(Type, "ResourceMovie")

        Type.addAction(Type, "CompositionNameSlider")
        Type.addAction(Type, "CompositionNameBar")

        Type.addAction(Type, "IsHorizontal")
        Type.addAction(Type, 'Value', Activate=True, Update=Movie2Scrollbar.__updateValue)

    def __init__(self):
        super(Movie2Scrollbar, self).__init__()

        self._slider = None
        self._bar = None

        self.tc = None

        self._slider_box = None
        self._slider_size = Mengine.vec2f(0.0, 0.0)
        self._half_slider_size = Mengine.vec2f(0.0, 0.0)
        self._bar_box = None
        pass

    def _onInitialize(self, obj):
        super(Movie2Scrollbar, self)._onInitialize(obj)

        if Mengine.hasResource(self.ResourceMovie) is False:
            Trace.log("Entity", 0, "Movie2Scrollbar._onInitialize: not found resource %s" % (self.ResourceMovie))
            return False

        resource = Mengine.getResourceReference(self.ResourceMovie)

        def __create_movie(name, composition_name, enable):
            if resource.hasComposition(composition_name) is False:
                return None

            movie = ObjectManager.createObjectUnique("Movie2", name, self.object,
                                                     ResourceMovie=self.ResourceMovie,
                                                     CompositionName=composition_name,
                                                     Interactive=True)
            self.addChild(movie.getEntityNode())

            movie.setEnable(enable)
            return movie

        self._bar = __create_movie('Bar', self.CompositionNameBar, True)
        # self._bar_resource = Mengine.getResourceReference(self.ResourceMovieBar)

        self._slider = __create_movie('Slider', self.CompositionNameSlider, True)
        # self._slider_resource = Mengine.getResourceReference(self.ResourceMovieSlider)

        # slot = self._bar.getMovieSlot('slider')
        # slot.addChild(self._content.getEntityNode())

        return True

    def getSliderMovie(self):
        return self._slider

    def getBarMovie(self):
        return self._bar

    def _onFinalize(self):
        super(Movie2Scrollbar, self)._onFinalize()

        self._bar.onDestroy()
        self._bar = None

        self._slider.onDestroy()
        self._slider = None
        pass

    def __updateValue(self, value):
        self.set_percentage(value)

    def get_percentage(self):
        socket_pos = self._slider.getSocket('socket').getWorldPolygonCenter()

        if self.object.getIsHorizontal() is True:
            return (socket_pos.x - self._bar_box.minimum.x - self._half_slider_size.x) / (self._bar_box.maximum.x - self._bar_box.minimum.x - self._slider_size.x)
        else:
            return (socket_pos.y - self._bar_box.minimum.y - self._half_slider_size.y) / (self._bar_box.maximum.y - self._bar_box.minimum.y - self._slider_size.y)

    def set_percentage(self, percent):
        movie = self._slider.getMovie()
        movie_pos = movie.getWorldPosition()
        socket_pos = movie.findSocket('socket').getWorldPolygonCenter()
        diff = (movie_pos.x - socket_pos.x, movie_pos.y - socket_pos.y)

        if self.object.getIsHorizontal() is True:
            movie.setWorldPosition((percent * (self._bar_box.maximum.x - self._bar_box.minimum.x - self._slider_size.x) + self._bar_box.minimum.x + self._half_slider_size.x + diff[0], movie_pos.y))
        else:
            movie.setWorldPosition((movie_pos.x, percent * (self._bar_box.maximum.y - self._bar_box.minimum.y - self._slider_size.y) + self._bar_box.minimum.y + self._half_slider_size.y + diff[1]))

    def _is_inside_bar(self, x, y):
        if self.object.getIsHorizontal() is True:
            left_offset = self._bar_box.minimum.x + self._half_slider_size.x - x
            if left_offset > 0:
                return Mengine.vec2f(left_offset, 0)
            else:
                right_offset = self._bar_box.maximum.x - self._half_slider_size.x - x
                if right_offset < 0:
                    return Mengine.vec2f(right_offset, 0)
        else:
            top_offset = self._bar_box.minimum.y + self._half_slider_size.y - y
            if top_offset > 0:
                return Mengine.vec2f(0, top_offset)
            else:
                bottom_offset = self._bar_box.maximum.y - self._half_slider_size.y - y
                if bottom_offset < 0:
                    return Mengine.vec2f(0, bottom_offset)

        return None

    def _move(self, dx, dy):
        x, y, _ = self._slider.getPosition()
        socket_pos = self._slider.getSocket('socket').getWorldPolygonCenter()

        if self.object.getIsHorizontal() is True:
            x += dx
            socket_pos.x += dx
        else:
            y += dy
            socket_pos.y += dy

        offset = self._is_inside_bar(socket_pos.x, socket_pos.y)
        if offset is None:
            self._slider.setPosition((x, y, _))
        else:
            self._slider.setPosition((x + offset.x, y + offset.y, _))

        self.object.onScroll(self.get_percentage())

    def _on_mouse_down(self):
        pass

    def _on_mouse_move(self, event):
        self._move(event.worldDelta.x, event.worldDelta.y)

    def _on_mouse_up(self):
        self.object.onScrollEnd(self.get_percentage())
        pass

    def _on_bar_click(self):
        mouse_pos = Mengine.getCursorPosition()
        socket_pos = self._slider.getSocket('socket').getWorldPolygonCenter()
        if self.object.getIsHorizontal() is True:
            self._move(mouse_pos.x - socket_pos.x, 0.0)
        else:
            self._move(0.0, mouse_pos.y - socket_pos.y)

    def _onActivate(self):
        self._mouse_handler = Mengine.addMouseMoveHandler(self._on_mouse_move)
        Mengine.enableGlobalHandler(self._mouse_handler, False)

        # self._slider_box = self._slider.getSocket('socket').getBoundingBox()
        # self._bar_box = self._bar.getSocket('socket').getBoundingBox()

        self._slider_box = Mengine.getHotSpotPolygonBoundingBox(self._slider.getSocket('socket'))
        self._bar_box = Mengine.getHotSpotPolygonBoundingBox(self._bar.getSocket('socket'))

        self._slider_size.set(self._slider_box.maximum.x - self._slider_box.minimum.x,
                              self._slider_box.maximum.y - self._slider_box.minimum.y)

        self._half_slider_size = self._slider_size * 0.5

        self.tc = TaskManager.createTaskChain(Repeat=True)
        with self.tc as tc:
            with tc.addRaceTask(2) as (slider, bar):
                bar.addTask('TaskMovie2SocketClick', Movie2=self._bar, SocketName='socket', isDown=True)
                bar.addFunction(self._on_bar_click)
                bar.addFunction(self._on_mouse_up)

                slider.addTask('TaskMovie2SocketClick', Movie2=self._slider, SocketName='socket', isDown=True)
                slider.addFunction(self._on_mouse_down)
                slider.addFunction(Mengine.enableGlobalHandler, self._mouse_handler, True)
                slider.addTask('TaskMouseButtonClick', isDown=False)
                slider.addFunction(Mengine.enableGlobalHandler, self._mouse_handler, False)
                slider.addFunction(self._on_mouse_up)

        self.set_percentage(0)

    def _onDeactivate(self):
        super(Movie2Scrollbar, self)._onDeactivate()

        if self._mouse_handler is not None:
            Mengine.removeGlobalHandler(self._mouse_handler)
            self._mouse_handler = None

        if self.tc is not None:
            self.tc.cancel()
            self.tc = None
        pass
    pass