from GOAP2.Initializer import Initializer

class AnimationSynchronizer(Initializer):
    def __init__(self):
        super(AnimationSynchronizer, self).__init__()
        self.animations = []
        self.timing = None

    def _onInitialize(self, animations=None):
        if animations is None:
            return

        for animation in animations:
            self.addAnimation(animation)

    def _onFinalize(self):
        self.animations = []
        self.timing = None

    def addAnimation(self, animation):
        self.animations.append(animation)

    def setTiming(self, timing):
        self.timing = timing

    def getTiming(self):
        return self.timing

    def saveTiming(self):
        for animation in self.animations:
            entity = animation.getEntity()
            movie = entity.getMovie()

            if movie.isActivate() is True:
                movie_animation = movie.getAnimation()
                timing = movie_animation.getTime()

                self.setTiming(timing)
                break

    def syncTiming(self):
        if self.timing is None:
            return

        for animation in self.animations:
            timing = self.getTiming()

            animation.setParam("StartTiming", timing)