from Foundation.Task.MixinObjectTemplate import MixinAnimation
from Foundation.Task.TaskObjectAnimatableEnd import TaskObjectAnimatableEnd

class TaskAnimationEnd(MixinAnimation, TaskObjectAnimatableEnd):
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