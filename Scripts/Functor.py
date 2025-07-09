class FunctorStore(object):
    __slots__ = "fn", "args", "kwargs"

    def __init__(self, fn, args, kwargs):
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        pass

    def __call__(self, *args, **kwargs):
        len_other_kwargs = len(kwargs)
        len_self_kwargs = len(self.kwargs)
        len_args = len(args)

        if len_other_kwargs == 0 and len_self_kwargs == 0:
            if len_args == 0:
                return self.fn(*self.args)
                pass
            else:
                return self.fn(*(args + self.args))
                pass
            pass
        elif len_other_kwargs == 0:
            if len_args == 0:
                return self.fn(*self.args, **self.kwargs)
                pass
            else:
                return self.fn(*(args + self.args), **self.kwargs)
                pass
            pass
        elif len_self_kwargs == 0:
            if len_args == 0:
                return self.fn(*self.args, **kwargs)
                pass
            else:
                return self.fn(*(args + self.args), **kwargs)
                pass
            pass
        else:
            newkeywords = kwargs.copy()
            newkeywords.update(self.kwargs)

            if len_args == 0:
                return self.fn(*self.args, **newkeywords)
                pass
            else:
                return self.fn(*(args + self.args), **newkeywords)
                pass
            pass
        pass

    def __repr__(self):
        return "<Functor fn '%s' args '%s' kwargs '%s'>" % (self.fn, self.args, self.kwargs)
        pass
    pass

class Functor(FunctorStore):
    def __init__(self, fn, *args, **kwargs):
        FunctorStore.__init__(self, fn, args, kwargs)
        pass
    pass