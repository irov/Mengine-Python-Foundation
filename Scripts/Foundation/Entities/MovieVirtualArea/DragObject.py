from Foundation.Entities.MovieVirtualArea.ElasticityEffect import ElasticityEffect
from Foundation.Entities.MovieVirtualArea.FrictionEffect import FrictionEffect
from Foundation.Entities.MovieVirtualArea.SnappingEffect import SnappingEffect
from Foundation.Vector2D import Vector2D
from Foundation.Vector4D import Vector4D

class DragObject(object):

    def _none_mode(self, x, y):
        return 0.0, 0.0

    def _free_mode(self, x, y):
        return x, y

    def _horizontal_mode(self, x, y):
        if self._scale_factor < 1.0:
            return x, y
        return x, 0.0

    def _vertical_mode(self, x, y):
        if self._scale_factor < 1.0:
            return x, y
        return 0.0, y

    def __init__(self, friction, rigidity, dragging_mode, max_scale, disable_drag_if_invalid,
                 drag_start_threshold, allow_out_of_bounds):
        self._modes = {
            'none': self._none_mode,
            'free': self._free_mode,
            'horizontal': self._horizontal_mode,
            'vertical': self._vertical_mode
        }
        try:
            self._initial_dragging_mode = self._dragging_mode = self._modes[dragging_mode]
        except KeyError:
            raise TypeError('"%s" dragging mode is not supported' % dragging_mode)

        self._on_position_changed = None

        self._dt = 0.0
        self._old_time = 0.0
        self._epsilon = 20.0

        self._start_drag_position = Vector2D()
        self._drag_start_threshold = drag_start_threshold

        self._position = Vector2D()
        self._velocity = Vector2D()

        self._velocity_limit = 150.0
        self._velocity_mouse_release_factor = 0.05

        self._scale_factor = 1.0
        self._max_scale = 1.0 / max_scale

        self._affector = None

        self._bounds = dict(begin=Vector2D(), end=Vector2D())
        self._local_bounds = dict(begin=Vector2D(), end=Vector2D())

        self._size = Vector4D()
        self._anchor_point = Vector2D()

        self._disable_drag = disable_drag_if_invalid
        self._allow_out_of_bounds = allow_out_of_bounds

        self._elasticity = ElasticityEffect(self, rigidity)
        self._friction = FrictionEffect(self, friction)
        self._snapping = SnappingEffect(self)

    def on_position_changed(self, callback):
        self._on_position_changed = callback

    def setup_affector(self):
        self.remove_affector()
        if self._dragging_mode is not self._modes['none']:
            self._affector = Mengine.addAffector(self._mouse_released_affector)

    def remove_affector(self):
        if self._affector is not None:
            Mengine.removeAffector(self._affector)
            self._affector = None

    def get_velocity(self):
        return Vector2D(self._velocity)

    def set_velocity(self, *args, **kwargs):
        if 'speed' in kwargs:
            kwargs['abs'] = kwargs['speed']
            del kwargs['speed']
        self._velocity.set(*args, **kwargs)

    def get_position(self):
        return Vector2D(self._position)

    def set_position(self, *args, **kwargs):
        self._position.set(*args, **kwargs)
        self._on_position_changed(self._position.x, self._position.y)

    def set_scale(self, scale):
        scale_factor = scale / self._scale_factor
        self.scale(scale_factor)

    def scale(self, scale_factor):
        scaled_factor = scale_factor * self._scale_factor
        if scaled_factor > 1.0:
            scale_factor = 1.0 / self._scale_factor
        elif scaled_factor < self._max_scale:
            scale_factor = self._max_scale / self._scale_factor

        center = (self._bounds['begin'] + self._bounds['end']) / 2.0

        size = (self._bounds['end'] - self._bounds['begin'])
        scaled_size = size * scale_factor

        half_scaled_size = scaled_size / 2.0

        self._scale_factor *= scale_factor
        self._bounds['begin'].set(center - half_scaled_size)
        self._bounds['end'].set(center + half_scaled_size)

        self._update_local_bounds()

        if self._allow_out_of_bounds is True:
            # do elasticity as usual
            self.setup_affector()
        else:
            # adjust position to viewport bounds
            offset = self._get_bounds_offset(self._position)
            self._move(offset)

    def set_anchor_point(self, *args, **kwargs):
        self._anchor_point.set(*args, **kwargs)
        self._update_local_bounds()
        self._update_position_to_anchor()

    def set_bounds(self, left, top, right, bottom):
        self._bounds['begin'].set(left, top)
        self._bounds['end'].set(right, bottom)

        self._update_local_bounds()
        self._update_position_to_anchor()
        self._validate_content_size()

    def get_bounds_viewport(self):
        return Mengine.Viewport((self._bounds['begin'].x, self._bounds['begin'].y),
                                (self._bounds['end'].x, self._bounds['end'].y))

    def get_bounds(self):
        return dict(self._bounds)

    def get_local_bounds(self):
        return dict(self._local_bounds)

    def set_content_size(self, left, top, right, bottom):
        self._size.set(left, top, right, bottom)
        self._validate_content_size()

    def get_content_size(self):
        return Vector4D(self._size)

    def _update_local_bounds(self):
        self._local_bounds['begin'] = self._bounds['begin'] - self._anchor_point
        self._local_bounds['end'] = self._bounds['end'] - self._anchor_point

    def _update_position_to_anchor(self):
        self.set_position(self._local_bounds['begin'])

    def _validate_content_size(self):
        vp_size = self._bounds['end'] - self._bounds['begin']
        invalid_width = abs(self._size.z - self._size.x) < vp_size.x
        invalid_height = abs(self._size.w - self._size.y) < vp_size.y

        if invalid_width and _DEVELOPMENT:
            Trace.msg_err("[Invalid width] VirtualArea width must be less then Content "
                          "(c.width {} < {} va.width)".format(abs(self._size.z - self._size.x), vp_size.x))
        if invalid_height and _DEVELOPMENT:
            Trace.msg_err("[Invalid height] VirtualArea height must be less then Content "
                          "(c.height {} < {} va.height)".format(abs(self._size.w - self._size.y), vp_size.y))

        if invalid_width and invalid_height:
            self._size.set(self._bounds['begin'].x, self._bounds['begin'].y, self._bounds['end'].x, self._bounds['end'].y)

            if self._disable_drag:
                self._dragging_mode = self._modes['none']

        elif invalid_width:
            self._size.set(x=self._bounds['begin'].x, z=self._bounds['end'].x)

            if self._disable_drag:
                if self._dragging_mode is self._modes['horizontal']:
                    self._dragging_mode = self._modes['none']

        elif invalid_height:
            self._size.set(y=self._bounds['begin'].y, w=self._bounds['end'].y)

            if self._disable_drag:
                if self._dragging_mode is self._modes['vertical']:
                    self._dragging_mode = self._modes['none']

        elif self._disable_drag:
            self._dragging_mode = self._initial_dragging_mode

    def _move(self, vec):
        self.set_position(self._position + vec)

    def _get_bounds_offset(self, position):
        """
        This method checks for target in specified position to being inside the viewport
        In case it's outside: the return value is vector that represents offsets by two axis
        Otherwise: Vector2D.Null is returned
        :param position: Vector2D instance
        :return: Vector2D instance
        """
        offset = Vector2D()

        sw = self._size.z - self._size.x
        sh = self._size.w - self._size.y

        right_offset = self._local_bounds['begin'].x - (position.x + self._size.x)
        left_offset = self._local_bounds['end'].x - (position.x + self._size.z)
        top_offset = self._local_bounds['begin'].y - (position.y + self._size.y)
        bottom_offset = self._local_bounds['end'].y - (position.y + self._size.w)

        offset.set(x=right_offset if right_offset < 0.0 else left_offset if left_offset > 0.0 else 0.0,

            y=top_offset if top_offset < 0.0 else bottom_offset if bottom_offset > 0.0 else 0.0)

        return offset

    def _mouse_released_affector(self, dt):
        """
        Almost all physics encapsulated inside this method 
        :param dt: time between frames
        :return: True when system get balanced
        """

        # checking for target being inside viewport
        offset = self._get_bounds_offset(self._position)
        if offset == Vector2D.Null:
            # target is inside the viewport in this case
            # adding snapping force
            self._snapping.pre_solve(dt)
            # adding friction force
            self._friction.pre_solve(dt)
        else:
            # target is outside the viewport in this case
            if self._allow_out_of_bounds is False:
                # print "!!! OUT OF BOUNDS - STOP !!!"
                self._move(offset)  # fix https://wonderland-games.atlassian.net/browse/AND-140
                return True
            # adding elasticity force
            self._elasticity.pre_solve(offset, dt)

        # calculating new position of target
        new_position = self._position + self._velocity * dt

        if offset == Vector2D.Null:
            # target was inside the viewport in this case
            if self._snapping.post_solve(new_position, dt):  # and self._friction.post_solve(dt):
                return True
            if self._friction.post_solve(dt):
                # print 'fricted'
                return True
        else:
            # target was outside the viewport in this case
            if self._elasticity.post_solve(offset, new_position, dt):
                # print 'elasticed'
                return True

        self.set_position(new_position)

        return False

    def mouse_move(self, touch_id, x, y, dx, dy):
        self._velocity.set(*self._dragging_mode(dx * self._scale_factor, dy * self._scale_factor))

        if self._allow_out_of_bounds is False:
            next_pos = self._position + self._velocity
            if self._get_bounds_offset(next_pos) != Vector2D.Null:
                self._velocity.set(0.0, 0.0)
                # print "!!!!! OUT OF BOUNDS"
                return

        offset = self._get_bounds_offset(self._position)  # current offset
        if self._velocity * offset < 0.0:
            self._velocity.x *= (self._elasticity.limit - abs(offset.x)) / self._elasticity.limit
            self._velocity.y *= (self._elasticity.limit - abs(offset.y)) / self._elasticity.limit
        self._move(self._velocity)

        current_time = Mengine.getTimeMs()
        self._dt = current_time - self._old_time
        self._old_time = current_time

        # self._snapping.pre_solve(self._dt)

    def mouse_press(self, x, y):
        self._start_drag_position.set(x, y)

        self.remove_affector()
        self._old_time = Mengine.getTimeMs()

    def mouse_release(self):
        if self._dt == 0.0:
            self._velocity.set(0.0, 0.0)
        else:
            if abs(self._velocity) > self._velocity_limit:
                self._velocity.set(abs=self._velocity_limit)

            # before fix
            # self._velocity /= self._dt

            # fix for VA to the sky flying
            self._velocity *= self._velocity_mouse_release_factor

    def check_drag_start(self, x, y):
        # ignore vector parts to dragging mode
        calc_x, calc_y = self._dragging_mode(x, y)
        if calc_x == 0.0:  # ignore horizontal part
            x = self._start_drag_position.x
        if calc_y == 0.0:  # ignore vertical part
            y = self._start_drag_position.y

        last_position = Vector2D(x, y)
        length = abs(last_position - self._start_drag_position)

        if length < self._drag_start_threshold:
            return False

        return True