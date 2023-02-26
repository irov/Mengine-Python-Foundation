from GOAP2.Task.MixinObjectTemplate import MixinMovie2
from GOAP2.Task.TaskObjectAnimatablePlay import TaskObjectAnimatablePlay

class TaskMovie2Play(MixinMovie2, TaskObjectAnimatablePlay):
    Skiped = True

    def getAnimatable(self):
        return self.Movie2
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