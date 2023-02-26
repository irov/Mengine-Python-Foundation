from GOAP2.Task.MixinObjectTemplate import MixinAnimation
from GOAP2.Task.TaskObjectAnimatableStop import TaskObjectAnimatableStop

class TaskAnimationStop(MixinAnimation, TaskObjectAnimatableStop):
    Skiped = True

    def getAnimatable(self):
        return self.Animation
        pass

    def getAnimation(self):
        animatable = self.getAnimatable()

        if animatable is None:
            return None
            pass

        animation = animatable.getAnimation()

        return animation
        pass
    pass