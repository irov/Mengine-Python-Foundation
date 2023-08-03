class TraceManager(object):

    s_traceConfig = {}
    s_levelRange = range(5)

    @staticmethod
    def setDictionary(config):
        TraceManager.s_traceConfig = config

    @staticmethod
    def existIn(type):
        if type in TraceManager.s_traceConfig:
            return True

        return False

    @staticmethod
    def addTraces(names):
        for name in names:
            TraceManager.addTrace(name)

    @staticmethod
    def addTrace(name):
        if name in TraceManager.s_traceConfig:
            Trace.msg_dev("TraceManager.addType-> TypeName - '%s' already exist in TraceManager.s_traceConfig" % (name))
            return

        TraceManager.s_traceConfig[name] = 0

    @staticmethod
    def getLevel(name):
        if name not in TraceManager.s_traceConfig:
            Trace.msg_dev("TraceManager.getLevel-> TypeName - '%s' not in TraceManager.s_traceConfig" % (name))
            return

        return TraceManager.s_traceConfig[name]

    @staticmethod
    def setLevel(name, levelValue):
        if name not in TraceManager.s_traceConfig:
            Trace.msg_dev("TraceManager.setLevel-> TypeName - '%s' not in TraceManager.s_traceConfig" % (name))
            return

        if levelValue not in TraceManager.s_levelRange:
            Trace.msg_dev("TraceManager.setLevel-> LevelValue - '%s' not in TraceManager.s_levelRange" % (levelValue))
            return

        TraceManager.s_traceConfig[name] = levelValue

    @staticmethod
    def removeTrace(name):
        TraceManager.s_traceConfig.pop(name)
