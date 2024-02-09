from Foundation.Task.MixinObjectTemplate import MixinMovie2
from Foundation.Task.TaskObjectAnimatableResume import TaskObjectAnimatableResume


class TaskMovie2Resume(MixinMovie2, TaskObjectAnimatableResume):
    Skiped = True

    def getAnimatable(self):
        return self.Movie2

    def getAnimation(self):
        animatable = self.getAnimatable()

        if animatable is None:
            return None

        animation = animatable.getAnimation()

        return animation
