def nonlocals(**kwds):
    def wrapper(fn):
        fn.func_globals.update(kwds)
        return fn
        pass

    return wrapper
    pass