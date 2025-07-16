def nonlocals(**kwargs):
    def wrapper(fn):
        fn.func_globals.update(kwargs)
        return fn
        pass

    return wrapper
    pass