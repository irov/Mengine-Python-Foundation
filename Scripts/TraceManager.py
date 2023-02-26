class TraceManager(object):
    s_traceConfig = {}
    s_levelRange = range(5)

    @staticmethod
    def setDictionary(config):
        TraceManager.s_traceConfig = config
        pass

    @staticmethod
    def existIn(type):
        if type in TraceManager.s_traceConfig:
            return True
            pass

        return False
        pass

    @staticmethod
    def addTraces(names):
        for name in names:
            TraceManager.addTrace(name)
            pass
        pass

    @staticmethod
    def addTrace(name):
        if name in TraceManager.s_traceConfig:
            print
            "TraceManager.addType-> TypeName - '%s' already exist in TraceManager.s_traceConfig" % (name)
            return
            pass

        TraceManager.s_traceConfig[name] = 0
        pass

    @staticmethod
    def getLevel(name):
        if name not in TraceManager.s_traceConfig:
            print
            "TraceManager.getLevel-> TypeName - '%s' not in TraceManager.s_traceConfig" % (name)
            return
            pass

        return TraceManager.s_traceConfig[name]
        pass

    @staticmethod
    def setLevel(name, levelValue):
        if name not in TraceManager.s_traceConfig:
            print
            "TraceManager.setLevel-> TypeName - '%s' not in TraceManager.s_traceConfig" % (name)
            return
            pass

        if levelValue not in TraceManager.s_levelRange:
            print
            "TraceManager.setLevel-> LevelValue - '%s' not in TraceManager.s_levelRange" % (levelValue)
            return
            pass

        TraceManager.s_traceConfig[name] = levelValue
        pass

    @staticmethod
    def removeTrace(name):
        TraceManager.s_traceConfig.pop(name)
        pass
    pass