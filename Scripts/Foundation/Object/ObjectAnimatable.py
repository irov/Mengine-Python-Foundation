from Object import Object

class ObjectAnimatable(Object):
    @staticmethod
    def declareORM(Type):
        Object.declareORM(Type)

        Type.addConst(Type, "PlayOnActivate")
        Type.addParam(Type, "LastFrameOnPlay")
        Type.addParam(Type, "Play")
        Type.addParam(Type, "Pause")
        Type.addParam(Type, "Loop")
        Type.addParam(Type, "StartTiming")
        Type.addParam(Type, "LastFrame")
        pass

    def __init__(self):
        super(ObjectAnimatable, self).__init__()

        self.onAnimatableEnd = Event("onAnimatableEnd")
        pass

    def _onParams(self, params):
        super(ObjectAnimatable, self)._onParams(params)

        self.initConst("PlayOnActivate", params, False)
        self.initParam("LastFrameOnPlay", params, False)

        self.initParam("Play", params, False)
        self.initParam("Pause", params, False)
        self.initParam("Loop", params, False)

        self.initParam("StartTiming", params, None)
        self.initParam("LastFrame", params, False)
        pass
    pass