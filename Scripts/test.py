class A(object):
    T = 0

    def __init__(self, v):
        if v is True:
            self.T = 2
            pass
        pass

class B(A):
    T = 1

    def __init__(self, v):
        super(B, self).__init__(v)
        pass
    pass

a = A(False)
b = B(False)
c = A(True)

print
a.T
print
b.T
print
c.T