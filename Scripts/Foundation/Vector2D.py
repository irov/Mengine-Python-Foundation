import math

class Vector2D(object):
    __slots__ = ('x', 'y')

    class Null(object):
        def __init__(self):
            self._null_vector = Vector2D()

        def __set__(self, instance, value):
            raise AttributeError('\'Vector2D\' object has no attribute \'Null\'')

        def __get__(self, instance, owner):
            if instance is not None:
                raise AttributeError('\'Vector2D\' object has no attribute \'Null\'')
            return self._null_vector

        def __delete__(self, instance):
            raise AttributeError('\'Vector2D\' object has no attribute \'Null\'')

    def __init__(self, x=None, y=None):
        x = x if x is not None else 0.0
        y = y if y is not None else 0.0

        if isinstance(x, Vector2D):
            self.x, self.y = x.x, x.y
        elif isinstance(x, tuple) and len(x) == 2:
            self.x, self.y = x[0], x[1]
        elif isinstance(x, list) and len(x) == 2:
            self.x, self.y = x[0], x[1]
        else:
            self.x, self.y = x, y
            pass

    def set(self, x=None, y=None, abs=None):
        x = x if x is not None else self.x
        y = y if y is not None else self.y

        if isinstance(x, Vector2D):
            self.x, self.y = x.x, x.y
        elif isinstance(x, tuple) and len(x) == 2:
            self.x, self.y = x[0], x[1]
        elif isinstance(x, list) and len(x) == 2:
            self.x, self.y = x[0], x[1]
        else:
            self.x, self.y = x, y
            pass

        if abs is not None:
            abs /= self.__abs__()
            self.x *= abs
            self.y *= abs
            pass
        pass

    def unit(self):
        mod = self.__abs__()
        if mod == 0:
            return Vector2D.Null
        return Vector2D(self.x / mod, self.y / mod)

    def __abs__(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, Vector2D):
            return self.x * other.x + self.y * other.y

        return Vector2D(self.x * other, self.y * other)

    def __rmul__(self, other):
        return self * other

    def __div__(self, other):
        other = float(other)
        return Vector2D(self.x / other, self.y / other)

    def __neg__(self):
        return Vector2D(-self.x, -self.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __imul__(self, other):
        self.x *= other
        self.y *= other
        return self

    def __idiv__(self, other):
        other = float(other)
        self.x /= other
        self.y /= other
        return self

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not (self == other)

    def __str__(self):
        return 'Vector2D(x={}, y={}, abs={})'.format(self.x, self.y, self.__abs__())

    def __repr__(self):
        return '<%s>' % self.__str__()

Vector2D.Null = Vector2D.Null()