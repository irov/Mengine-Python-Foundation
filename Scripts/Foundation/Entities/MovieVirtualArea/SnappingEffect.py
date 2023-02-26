from Foundation.Vector2D import Vector2D

class SnappingEffect(object):

    def __init__(self, target):
        self._target = target
        self.bounds_point = Vector2D()
        self.axis = 'x'
        self.coefficient = 0.0001
        self._epsilon = 2.0
        self._acceleration = Vector2D()
        self._distance = 0.0

        self._snappers = []

    def set_to_X_axis(self):
        self.axis = 'x'

    def set_to_Y_axis(self):
        self.axis = 'y'

    def set_bounds_point(self, bounds_point):
        self.bounds_point = self._target._bounds['begin'] + bounds_point

    def add_snapper(self, content_point):
        self._snappers.append(getattr(self._target._anchor_point, self.axis) + content_point)

    def get_nearest_point(self, position=0):
        min_distance = getattr(self.bounds_point, self.axis) - (position + self._snappers[0])
        for i, snapper in enumerate(self._snappers[1:], 1):
            distance = getattr(self.bounds_point, self.axis) - (position + snapper)
            if abs(distance) < abs(min_distance):
                min_distance = distance
        return min_distance

    def pre_solve(self, dt):
        if len(self._snappers) == 0:
            return
        self._distance = self.get_nearest_point(getattr(self._target._position, self.axis))
        self._acceleration = self.coefficient * self._snapping_law(self._distance)
        self._target._velocity += self._acceleration * dt

    def post_solve(self, position, dt):
        if len(self._snappers) == 0:
            # print 'no snappers'
            return False
        self._distance = self.get_nearest_point(getattr(self._target._position, self.axis))
        if abs(self._distance) <= self._epsilon:
            self._target.set_position(**{self.axis: getattr(self._target._position, self.axis) + self._distance})
            # print 'target was snapped'
            self._target.set_velocity(0, 0)
            return True
        return False

    def _snapping_law(self, distance):
        direction = Vector2D()
        direction.set(**{self.axis: distance})
        # direction.set(abs=distance)
        return direction