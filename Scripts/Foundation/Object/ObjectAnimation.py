from ObjectAnimatable import ObjectAnimatable

class ObjectAnimation(ObjectAnimatable):
    @staticmethod
    def declareORM(Type):
        ObjectAnimatable.declareORM(Type)

        Type.declareResource("AnimationResourceName")
        Type.declareParam("Sequence")
        Type.declareParam("FrameIndex")
        pass

    def _onParams(self, params):
        super(ObjectAnimation, self)._onParams(params)

        self.initResource("AnimationResourceName", params, None)
        self.initParam("Sequence", params, [(0, 0)])
        self.initParam("FrameIndex", params, 0)
        pass
    pass