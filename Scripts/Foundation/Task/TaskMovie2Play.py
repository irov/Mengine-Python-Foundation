from Foundation.Task.MixinObjectTemplate import MixinMovie2
from Foundation.Task.TaskObjectAnimatablePlay import TaskObjectAnimatablePlay

class TaskMovie2Play(MixinMovie2, TaskObjectAnimatablePlay):
    Skiped = True

    def getAnimatable(self):
        return self.Movie2

    def getAnimation(self):
        animatable = self.getAnimatable()

        if animatable is None:
            return None

        animation = animatable.getAnimation()

        return animation