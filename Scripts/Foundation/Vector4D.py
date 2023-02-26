class Vector4D(object):
    __slots__ = ('x', 'y', 'z', 'w')

    class Null(object):
        def __init__(self):
            self._null_vector = Vector4D()

        def __set__(self, instance, value):
            raise AttributeError('\'Vector4D\' object has no attribute \'Null\'')

        def __get__(self, instance, owner):
            if instance is not None:
                raise AttributeError('\'Vector4D\' object has no attribute \'Null\'')
            return self._null_vector

        def __delete__(self, instance):
            raise AttributeError('\'Vector4D\' object has no attribute \'Null\'')

    def __init__(self, x=None, y=None, z=None, w=None):
        x = x if x is not None else 0.0
        y = y if y is not None else 0.0
        z = z if z is not None else 0.0
        w = w if w is not None else 0.0

        if isinstance(x, Vector4D):
            self.x, self.y, self.z, self.w = x.x, x.y, x.z, x.w
        elif isinstance(x, tuple) and len(x) == 4:
            self.x, self.y, self.z, self.w = x[0], x[1], x[2], x[3]
        elif isinstance(x, list) and len(x) == 4:
            self.x, self.y, self.z, self.w = x[0], x[1], x[2], x[3]
        else:
            self.x, self.y, self.z, self.w = x, y, z, w

    def set(self, x=None, y=None, z=None, w=None):
        x = x if x is not None else self.x
        y = y if y is not None else self.y
        z = z if z is not None else self.z
        w = w if w is not None else self.w

        if isinstance(x, Vector4D):
            self.x, self.y, self.z, self.w = x.x, x.y, x.z, x.w
        elif isinstance(x, tuple) and len(x) == 4:
            self.x, self.y, self.z, self.w = x[0], x[1], x[2], x[3]
        elif isinstance(x, list) and len(x) == 4:
            self.x, self.y, self.z, self.w = x[0], x[1], x[2], x[3]
        else:
            self.x, self.y, self.z, self.w = x, y, z, w

    def __str__(self):
        return 'Vector4D(x={}, y={}, z={}, w={})'.format(self.x, self.y, self.z, self.w)

    def __repr__(self):
        return '<%s>' % self.__str__()

Vector4D.Null = Vector4D.Null()