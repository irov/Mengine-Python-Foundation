import math

from GOAP2.Vector2D import Vector2D

class FrictionEffect(object):
    Friction_Minimum = 0.001
    Friction_Maximum = 0.01

    def __init__(self, target, friction):
        self._target = target

        self._friction_coefficient = self.Friction_Minimum + (self.Friction_Maximum - self.Friction_Minimum) * friction
        self._acceleration = Vector2D()

    def pre_solve(self, dt):
        velocity = self._target._velocity
        self._acceleration = self._friction_coefficient * -velocity.unit() * self._friction_law(abs(velocity))
        self._target._velocity += self._acceleration * dt

    def post_solve(self, dt):
        return self._acceleration * self._target._velocity >= 0

    def _friction_law(self, speed):
        # if speed < self._epsilon:
        #     return 0

        return math.sqrt(speed) * self._target._scale_factor  # return speed