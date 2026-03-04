from Foundation.Task.MixinObjectTemplate import MixinAnimation
from Foundation.Task.TaskObjectAnimatableStop import TaskObjectAnimatableStop

class TaskAnimationStop(MixinAnimation, TaskObjectAnimatableStop):
    Skiped = True

    def getAnimatable(self):
        return self.Animation

    def getAnimation(self):
        animatable = self.getAnimatable()

        if animatable is None:
            return None

        animation = animatable.getAnimation()

        return animation
    pass