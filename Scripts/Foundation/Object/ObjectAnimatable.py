from Object import Object

class ObjectAnimatable(Object):
    @staticmethod
    def declareORM(Type):
        Object.declareORM(Type)

        Type.declareConst("PlayOnActivate")
        Type.declareParam("LastFrameOnPlay")
        Type.declareParam("Play")
        Type.declareParam("Pause")
        Type.declareParam("Loop")
        Type.declareParam("StartTiming")
        Type.declareParam("LastFrame")
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