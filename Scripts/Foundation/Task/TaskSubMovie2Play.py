# from Foundation.Task.MixinObjectTemplate import MixinMovie
from Foundation.Task.MixinObjectTemplate import MixinMovie2
from Foundation.Task.Task import Task

class TaskSubMovie2Play(MixinMovie2, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskSubMovie2Play, self)._onParams(params)

        self.SubMovieName = params.get("SubMovie2Name", None)
        self.Loop = params.get("Loop", None)
        self.Wait = params.get("Wait", True)

    def _onInitialize(self):
        super(TaskSubMovie2Play, self)._onInitialize()
        self.playId = None
        pass

    def getAnimatable(self):
        return self.Movie2
        pass

    def _onValidate(self):
        super(TaskSubMovie2Play, self)._onValidate()

        Animatable = self.getAnimatable()

        if Animatable is None:
            self.validateFailed("Animatable is None")

        if self.SubMovieName is None:
            self.validateFailed("SubMovieName is None")

        Entity = Animatable.getEntity()

        if Entity is None:
            self.validateFailed("Animatable {} has no Entity".format(Animatable.getName()))

        if Entity.hasSubMovie(self.SubMovieName) is False:
            self.validateFailed("Animatable {} has no submovie {}".format(Animatable.getName(), self.SubMovieName))

    def _onRun(self):
        Animatable = self.getAnimatable()

        if self.SubMovieName in Animatable.getParam('LastFrameSubMovies'):
            Animatable.delParam('LastFrameSubMovies', self.SubMovieName)

        Entity = Animatable.getEntity()

        SubMovie = Entity.getSubMovie(self.SubMovieName)

        Animation = SubMovie.getAnimation()

        if self.Loop is not None:
            Animation.setLoop(self.Loop)
            pass

        self.playId = Animation.play()

        if self.playId == 0:
            self.log("animation play: %s invalid start play" % (Animation))
            self.end()
            return True

        if self.Wait is False:
            return True
            pass

        SubMovie.setEventListener(onAnimatableEnd=self.__onAnimatableEnd)

        return False
        pass

    def _onSkip(self):
        super(TaskSubMovie2Play, self)._onSkip()
        self.end()
        pass

    def __onAnimatableEnd(self, id):
        if self.playId != id:
            return
            pass

        self.end()
        pass

    def end(self):
        Animatable = self.getAnimatable()
        Animatable.appendParam('LastFrameSubMovies', self.SubMovieName)

        if Animatable.isActive():
            Entity = Animatable.getEntity()

            if Entity is not None:
                SubMovie = Entity.getSubMovie(self.SubMovieName)
                SubMovie.setEventListener(onAnimatableEnd=None)

        self.complete()