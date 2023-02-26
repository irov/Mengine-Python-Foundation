from GOAP2.Task.MixinObjectTemplate import MixinMovie2
from GOAP2.Task.TaskObjectAnimatableEnd import TaskObjectAnimatableEnd

class TaskMovie2End(MixinMovie2, TaskObjectAnimatableEnd):
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