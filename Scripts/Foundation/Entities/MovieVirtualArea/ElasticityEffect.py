from Foundation.Vector2D import Vector2D

class ElasticityEffect(object):
    Rigidity_Minimum = 100.0
    Rigidity_Maximum = 1000.0

    def __init__(self, target, rigidity):
        self._target = target

        self.coefficient = 0.045
        self.limit = self.Rigidity_Minimum + (self.Rigidity_Maximum - self.Rigidity_Minimum) * (1.0 - rigidity)

    def pre_solve(self, offset, dt):
        acceleration = self.coefficient * self._elasticity_law(offset)
        self._target._velocity += acceleration * dt

    def post_solve(self, offset, new_position, dt):
        target = self._target
        new_offset = target._get_bounds_offset(new_position)
        if new_offset == Vector2D.Null:
            # target became inside the viewport in this case
            target.set_position(target._position + offset)
            target._velocity.set(0.0, 0.0)
            return True
        else:
            # target became outside the viewport in this case
            if new_offset.x == 0.0 and offset.x != 0.0 or new_offset.x * offset.x < 0.0:
                # target returned to bounds by X-axis
                new_position.set(x=target._position.x + offset.x)
                target._velocity.set(x=0.0)
            elif new_offset.y == 0.0 and offset.y != 0.0 or new_offset.y * offset.y < 0.0:
                # target returned to bounds by Y-axis
                new_position.set(y=target._position.y + offset.y)
                target._velocity.set(y=0.0)

        return False

    def _elasticity_law(self, offset):
        # x = self.elasticity_limit - abs(offset.x)
        # y = self.elasticity_limit - abs(offset.y)
        return offset / self.limit