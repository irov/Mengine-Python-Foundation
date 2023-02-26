def abstract(func):
    def closure(*dt, **mp):
        raise NotImplementedError("Method %s is pure virtual" % func.__name__)
    return closure