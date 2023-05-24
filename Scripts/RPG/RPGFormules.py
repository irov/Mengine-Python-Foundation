import math

class RPGFormules(object):
    def __init__(self):
        self.formules = {}
        pass

    def addFormula(self, name, code):
        f = self.__makeFormulaCode(name, code)

        self.formules[name] = f
        pass

    def hasFormula(self, name):
        return name in self.formules
        pass

    def calcFormula(self, name, Value=None, Global=None, **Other):
        f = self.formules.get(name)

        if f is None:
            return None
            pass

        def __rand(value):
            return Mengine.randf(value)
        def __fibo(value):
            return Mengine.fibo_bine(value)
        def __log10(value):
            return Mengine.log10f(value)
        def __resist(value):
            return (1.0 - (0.06 * value) / (1.0 + 0.06 * value)) if value >= 0.0 else 1.0 / (1.0 - pow(0.94, -value))
        def __evade(value):
            return 1.0 if Mengine.randf(100.0) <= value else 0.0
        def __sum(value):
            return sum(value)
        def __ceil(value):
            return math.ceil(value)
        def __floor(value):
            return math.floor(value)

        sandbox = dict(Value=Value, rand=__rand, fibo=__fibo, log10=__log10, Resist=__resist, Evade=__evade, sum=__sum,
                       ceil=__ceil, floor=__floor)

        if Global is not None:
            sandbox.update(Global)
            pass

        sandbox.update(Other)

        try:
            exec(f, sandbox)
        except Exception as ex:
            Trace.log("Utils", 0, "ex: function %s error: %s" % (name, ex))

            return None
            pass

        result = sandbox["Result"]

        return result
        pass

    def __makeFormulaCode(self, name, code):
        true_code = "Result = %s" % (code)

        c = compile(true_code, '<string>', 'exec')

        return c
        pass
    pass