from Foundation.Task.MixinObjectTemplate import MixinMovie2
from Foundation.Task.TaskObjectAnimatablePause import TaskObjectAnimatablePause


class TaskMovie2Pause(MixinMovie2, TaskObjectAnimatablePause):
    Skiped = True

    def getAnimatable(self):
        return self.Movie2

    def getAnimation(self):
        animatable = self.getAnimatable()

        if animatable is None:
            return None

        animation = animatable.getAnimation()

        return animation
