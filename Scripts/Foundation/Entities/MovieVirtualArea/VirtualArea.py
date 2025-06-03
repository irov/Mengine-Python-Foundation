from Foundation.Initializer import Initializer

from DragObject import DragObject

class VirtualArea(Initializer):

    def __init__(self):
        super(VirtualArea, self).__init__()

        self._enable_scale = False
        self._scale_factor = None
        self._is_scaling = False

        self._target = None

        # input handlers
        self._mouse_wheel_handler = None
        self._mouse_press_handler = None
        self._mouse_move_handler = None
        self._mouse_release_handler = None
        self._mouse_leave_handler = None
        self._socket = None

        self._root = None

        self._camera = None
        self._viewport = None

        self._is_dragging = False
        self._start_drag_position = None

        self._frozen = False

        self._touch_ids = {}  # { touch_id : event }

        # events
        self.on_drag = None
        self.on_drag_start = None
        self.on_drag_move = None
        self.on_drag_end = None
        self.on_scale = None
        self.on_touch = None

    def _onInitialize(self, *args, **kwargs):
        enable_scale = kwargs.get('enable_scale', True)
        scale_factor = kwargs.get('scale_factor', 0.375)
        viewport = kwargs.get('viewport_node', None)
        content_size = kwargs.get('content_size', (0.0, 0.0, 2736.0, 1536.0))
        drag_object_params = {
            "friction": kwargs.get('friction', 0.5),
            "rigidity": kwargs.get('rigidity', 0.5),
            "dragging_mode": kwargs.get('dragging_mode', 'free'),
            "max_scale": kwargs.get('max_scale', 6.0),
            "disable_drag_if_invalid": kwargs.get('disable_drag_if_invalid', True),
            "drag_start_threshold": kwargs.get('drag_start_threshold', 50.0),  # todo: px -> cm
            "allow_out_of_bounds": kwargs.get('allow_out_of_bounds', True)
        }
        name = kwargs.get('name', 'VirtualArea')
        camera_name = kwargs.get('camera_name', 'VirtualAreaRenderCameraOrthogonal')
        viewport_name = kwargs.get('viewport_name', 'VirtualAreaRenderViewport')

        self._enable_scale = enable_scale
        self._scale_factor = scale_factor

        self._target = DragObject(**drag_object_params)
        self._target.on_position_changed(self._set_position)
        self._target.set_content_size(*content_size)

        self._root = Mengine.createNode('Interender')
        self._root.setName(name)

        self._camera = self._root.createChild('RenderCameraOrthogonal')
        self._camera.setName(camera_name)
        self._viewport = self._root.createChild('RenderViewport')
        self._viewport.setName(viewport_name)

        if viewport:
            self.setup_viewport(viewport)
            pass

        root_render = self._root.getRender()
        root_render.setRenderViewport(self._viewport)
        root_render.setRenderCamera(self._camera)

        self.on_drag = Event('onDrag')
        self.on_drag_start = Event('onDragStart')
        self.on_drag_move = Event('onDragMove')
        self.on_drag_end = Event('onDragEnd')
        self.on_scale = Event('onScale')
        self.on_touch = Event('onTouch')

    def _onFinalize(self):
        if self._socket is not None:
            if self._mouse_wheel_handler is not None:
                self._socket.removeEventListener(self._mouse_wheel_handler)
                self._mouse_wheel_handler = None

            if self._mouse_press_handler is not None:
                self._socket.removeEventListener(self._mouse_press_handler)
                self._mouse_press_handler = None

        if self._mouse_move_handler is not None:
            Mengine.removeGlobalHandler(self._mouse_move_handler)
            self._mouse_move_handler = None

        if self._mouse_release_handler is not None:
            Mengine.removeGlobalHandler(self._mouse_release_handler)
            self._mouse_release_handler = None

        if self._mouse_leave_handler is not None:
            Mengine.removeGlobalHandler(self._mouse_leave_handler)
            self._mouse_leave_handler = None

        self.on_drag = None
        self.on_drag_start = None
        self.on_drag_move = None
        self.on_drag_end = None
        self.on_scale = None
        self.on_touch = None

        self._socket = None

        self._camera = None
        self._viewport = None

        if self._root is not None:
            root_render = self._root.getRender()
            root_render.setRenderViewport(None)
            root_render.setRenderCamera(None)

            self._root.removeFromParent()
            Mengine.destroyNode(self._root)
            self._root = None

        # finalize target
        self._target.remove_affector()

    def _set_position(self, x, y):
        """
        Called when target position was changed
        """
        self._camera.setLocalPositionX(-x)
        self._camera.setLocalPositionY(-y)
        self.on_drag(*self.get_percentage())

        if self.is_dragging() is True:
            self.on_drag_move(*self.get_percentage())

    def set_snapping(self, bounds, content, radius):
        self._target._snapping.set(bounds, content, radius)

    def get_snapping(self):
        return self._target._snapping

    def set_percentage(self, x=None, y=None):
        x_is_None = x is None
        y_is_None = y is None

        if x_is_None and y_is_None:
            raise TypeError

        bounds = self._target._local_bounds
        size = self._target._size
        self._target.set_velocity(Mengine.vec2f(0, 0))
        self._target.setup_affector()

        x = self._target.get_position().x if x is None else bounds['begin'].x + (self.get_width() - abs(size.x - size.z)) * x
        y = self._target.get_position().y if y is None else bounds['begin'].y + (self.get_height() - abs(size.y - size.w)) * y

        self._target.set_position(Mengine.vec2f(x, y))

    def get_percentage(self):
        position = self._target._position
        bounds = self._target._local_bounds
        size = self._target._size

        horizontal_gap = self.get_width() - abs(size.x - size.z)
        vertical_gap = self.get_height() - abs(size.y - size.w)

        def __adjust(_percent):
            if _percent < -1.0:
                return -1.0
            elif _percent > 1.0:
                return 1.0
            return _percent

        try:
            percent_x = __adjust((position.x - bounds['begin'].x) / horizontal_gap)
        except ZeroDivisionError:
            percent_x = 0
        try:
            percent_y = __adjust((position.y - bounds['begin'].y) / vertical_gap)
        except ZeroDivisionError:
            percent_y = 0

        return percent_x, percent_y

    def set_content_size(self, left, top, right, bottom):
        self._target.set_content_size(left, top, right, bottom)

    def get_content_size(self):
        return (self._target._size.x, self._target._size.y, self._target._size.z, self._target._size.w,)

    def get_width(self):
        return self._target._bounds['end'].x - self._target._bounds['begin'].x

    def get_height(self):
        return self._target._bounds['end'].y - self._target._bounds['begin'].y

    def get_socket(self):
        return self._socket

    def get_viewport(self):
        return self._viewport

    def set_anchor_point(self, *args, **kwargs):
        self._target.set_anchor_point(*args, **kwargs)

    def add_node(self, node, use_as_anchor=False):
        """
        Method for creating virtual area scene subtree.
        All nodes attached to this tree will be draggable and rendered inside viewport.
        :param node: Mengine.Node or its subclass
        :param use_as_anchor:
        :return: None
        """
        if use_as_anchor:
            anchor = node.getWorldPosition()
            self._target.set_anchor_point(anchor)
        self._root.addChild(node)

    def get_node(self):
        """
        Uses for adding virtual area to scene
        :return: root of virtual area tree
        """
        return self._root

    def get_touch_count(self):
        return len(self._touch_ids)

    def update_target(self):
        self._target.setup_affector()

    def is_dragging(self):
        return self._is_dragging

    def scale(self, scale_factor):
        """
        Scales target and camera
        """
        self._target.scale(scale_factor)

        vp = self._target.get_bounds_viewport()
        self._camera.setOrthogonalViewport(vp)
        self.on_scale(self._target.get_scale_factor())

    def set_scale(self, scale):
        """ Scales target and camera to specific `scale` value """
        scale_factor = scale / self._target.get_scale_factor()
        self.scale(scale_factor)

    def get_scale_factor(self):
        return self._target.get_scale_factor()

    def freeze(self, value):
        self._frozen = value
        Mengine.enableGlobalHandler(self._mouse_move_handler, False)
        Mengine.enableGlobalHandler(self._mouse_release_handler, False)
        Mengine.enableGlobalHandler(self._mouse_leave_handler, False)

    def setup_viewport(self, left, top=None, right=None, bottom=None):
        """
        Sets up the size of rendering viewport of virtual area.
        If first parameter is instance of Mengine.Node and other parameters is omitted -
        this method takes size of its bounding box by the 'getBoundingBox' method.
        :param left: can be the next types - (number, Mengine.Node, Mengine.Viewport).
            If this param is instance of Mengine.Viewport and others omitted
            then just sets up virtual area viewport by this one.
        :param top: number
        :param right: number
        :param bottom: number
        :return: None
        """
        def __set(vp):
            self._target.set_bounds(vp.begin.x, vp.begin.y, vp.end.x, vp.end.y, )
            self._viewport.setViewport(vp)

            self._camera.setOrthogonalViewport(vp)
            self._camera.setFixedOrthogonalViewport(True)

        if isinstance(left, Mengine.HotSpotPolygon):
            box = Mengine.getHotSpotPolygonBoundingBox(left)
            __set(Mengine.Viewport(box.minimum, box.maximum))

        elif isinstance(left, Mengine.Viewport):
            __set(left)

        elif all((top is not None, right is not None, bottom is not None)):
            __set(Mengine.Viewport((left, top), (right, bottom)))

        else:
            raise TypeError("Wrong type {}, should be number, Mengine.Node or Mengine.Viewport".format(type(left)))

    def init_handlers(self, hotspot):
        """
        Initializes handlers of dragging/scaling events
        :param movie: movie object with socket
        :param socket_name: to this socket will be attached listening of dragging/scaling events
        :return: None
        """
        def mouse_press(touch_id, x, y, _1, _2, is_down, _3):
            handle = self._socket.getDefaultHandle()
            if is_down:
                self.on_touch(touch_id)
                self._target.mouse_press(x, y)
                Mengine.enableGlobalHandler(self._mouse_move_handler, not self._frozen)
                Mengine.enableGlobalHandler(self._mouse_release_handler, not self._frozen)
                Mengine.enableGlobalHandler(self._mouse_leave_handler, not self._frozen)

            return handle

        def mouse_wheel(x, y, _, direction):
            handle = self._socket.getDefaultHandle()
            if direction > 0:
                self.scale(1.0 - self._scale_factor)
            else:
                self.scale(1.0 + self._scale_factor)

            return handle

        def _mouse_scale():
            if len(self._touch_ids) != 2:
                return
            if self._is_scaling is True:
                return
            self._is_scaling = True

            touch0 = self._touch_ids[0]
            touch1 = self._touch_ids[1]

            touch0_cur_pos = Mengine.vec2f(touch0.x, touch0.y)
            touch1_cur_pos = Mengine.vec2f(touch1.x, touch1.y)

            touch0_prev_pos = touch0_cur_pos + Mengine.vec2f(touch0.dx, touch0.dy)
            touch1_prev_pos = touch1_cur_pos + Mengine.vec2f(touch1.dx, touch1.dy)

            def magnitude(vec1, vec2):
                vec = (vec1 - vec2)
                return (vec.x ** 2 + vec.y ** 2) ** 0.5

            prev_magnitude = magnitude(touch0_prev_pos, touch1_prev_pos)
            cur_magnitude = magnitude(touch0_cur_pos, touch1_cur_pos)
            difference = cur_magnitude - prev_magnitude

            self.scale(1.0 + difference * self._scale_factor)
            self._is_scaling = False

        def mouse_move(event):
            # pinch technique - scale
            self._touch_ids[event.touchId] = event  # update
            if self._enable_scale is True:
                _mouse_scale()

            # scroll
            if len(self._touch_ids) != 1:
                if event.touchId in self._touch_ids:
                    self._touch_ids.pop(event.touchId)
                return

            if not self._is_dragging and self._target.check_drag_start(event.x, event.y) is True:
                self._is_dragging = True
                self.on_drag_start()

            if self._is_dragging is True:
                self._target.mouse_move(event.touchId, event.x, event.y, event.dx, event.dy)

        def mouse_release(event):
            if event.isDown is True:
                # just touched, not release
                return
            self.on_drag_end()
            self.__mouse_release(event)

        def mouse_leave(event):
            self.on_drag_end()
            self.__mouse_release(event)

        self._mouse_move_handler = Mengine.addMouseMoveHandler(mouse_move)
        self._mouse_release_handler = Mengine.addMouseButtonHandler(mouse_release)
        self._mouse_leave_handler = Mengine.addMouseLeaveHandler(mouse_leave)
        Mengine.enableGlobalHandler(self._mouse_move_handler, False)
        Mengine.enableGlobalHandler(self._mouse_release_handler, False)
        Mengine.enableGlobalHandler(self._mouse_leave_handler, False)

        self._socket = hotspot
        if self._enable_scale:
            self._mouse_wheel_handler = self._socket.setEventListener(onHandleMouseWheel=mouse_wheel)
        self._mouse_press_handler = self._socket.setEventListener(onHandleMouseButtonEvent=mouse_press)

    def setup_with_movie(self, movie, socket_name, slot_name=None):
        socket = movie.getSocket(socket_name)

        self.setup_viewport(socket)

        socket = movie.getSocket(socket_name)

        self.init_handlers(socket)

        attach_to_node = movie.getEntityNode()

        if slot_name is not None:
            slot = movie.getMovieSlot(slot_name)
            if slot is not None:
                attach_to_node = slot

        attach_to_node.addChild(self._root)

    def __mouse_release(self, event):
        if event.touchId in self._touch_ids:
            self._touch_ids.pop(event.touchId)

        self._is_dragging = False
        Mengine.enableGlobalHandler(self._mouse_move_handler, False)
        Mengine.enableGlobalHandler(self._mouse_release_handler, False)
        Mengine.enableGlobalHandler(self._mouse_leave_handler, False)
        self._target.mouse_release()
        self._target.setup_affector()