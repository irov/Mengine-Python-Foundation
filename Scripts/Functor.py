class FunctorStore(object):
    __slots__ = "fn", "args", "kwargs"

    def __init__(self, fn, args, kwargs):
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        pass

    def __call__(self, *args, **kwargs):
        len_other_args = len(args)
        len_other_kwargs = len(kwargs)
        len_self_args = 0 if self.args is None else len(self.args)
        len_self_kwargs = 0 if self.kwargs is None else len(self.kwargs)

        if len_other_kwargs == 0 and len_self_kwargs == 0:
            if len_other_args == 0 and len_self_args == 0:
                return self.fn()
            elif len_other_args == 0:
                return self.fn(*self.args)
            elif len_self_args == 0:
                return self.fn(*args)
            else:
                return self.fn(*(args + self.args))
        elif len_other_kwargs == 0:
            if len_other_args == 0 and len_self_args == 0:
                return self.fn(**self.kwargs)
            elif len_other_args == 0:
                return self.fn(*self.args, **self.kwargs)
            elif len_self_args == 0:
                return self.fn(*args, **self.kwargs)
            else:
                return self.fn(*(args + self.args), **self.kwargs)
        elif len_self_kwargs == 0:
            if len_other_args == 0 and len_self_args == 0:
                return self.fn(**kwargs)
            elif len_other_args == 0:
                return self.fn(*self.args, **kwargs)
            elif len_self_args == 0:
                return self.fn(*args, **kwargs)
            else:
                return self.fn(*(args + self.args), **kwargs)
        else:
            newkeywords = dict(kwargs, **self.kwargs)

            if len_other_args == 0 and len_self_args == 0:
                return self.fn(**newkeywords)
            elif len_other_args == 0:
                return self.fn(*self.args, **newkeywords)
            elif len_self_args == 0:
                return self.fn(*args, **newkeywords)
            else:
                return self.fn(*(args + self.args), **newkeywords)

    def __repr__(self):
        return "<Functor fn '%s' args '%s' kwargs '%s'>" % (self.fn, self.args, self.kwargs)

class Functor(FunctorStore):
    def __init__(self, fn, *args, **kwargs):
        FunctorStore.__init__(self, fn, args, kwargs)
        pass
    pass