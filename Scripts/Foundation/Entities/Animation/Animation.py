from Foundation.Entity.BaseAnimatable import BaseAnimatable

class Animation(BaseAnimatable):

    @staticmethod
    def declareORM(Type):
        BaseAnimatable.declareORM(Type)

        Type.addAction(Type, "Sequence", Update=Animation.__updateSequence)
        Type.addActionActivate(Type, "FrameIndex", Update=Animation.__updateFrameIndex)
        Type.addAction(Type, "AnimationResourceName")
        pass

    def __init__(self):
        super(Animation, self).__init__()

        self.animation = None
        pass

    def getAnimatable(self):
        return self.animation
        pass

    def getSprite(self):
        return self.animation
        pass

    def __updateFrameIndex(self, index):
        self.animation.setCurrentFrame(index)
        pass

    def __updateSequence(self, sequence):
        if sequence is None:
            return
            pass
        # sequenceID = "%s_%s"%(self.object.name, str(sequence))
        # Mengine.createAnimationSequence(sequenceID, sequence)
        # self.animation.setResourceAnimation(sequenceID)
        pass

    def getLastFrameIndexFromSequence(self, sequence):
        return sequence[len(sequence) - 1][1]
        pass

    def _onInitialize(self, obj):
        super(Animation, self)._onInitialize(obj)

        self.animation = self.createChild("Animation")
        self.animation.setResourceAnimation(self.AnimationResourceName)
        self.animation.setEventListener(onAnimationEnd=self.__onAnimationEnd)
        self.animation.enable()
        pass

    def _onFinalize(self):
        super(Animation, self)._onFinalize()

        Mengine.destroyNode(self.animation)
        self.animation = None
        pass

    def __onAnimationEnd(self, emitter, id, isEnd):
        if self.validPlayId(id) is False:
            return

        self.end()
        pass

    def _onStop(self):
        pass
    pass