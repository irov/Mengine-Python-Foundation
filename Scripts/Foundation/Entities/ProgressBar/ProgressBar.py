from Foundation.Entity.BaseEntity import BaseEntity

class ProgressBar(BaseEntity):
    @staticmethod
    def declareORM(Type):
        BaseEntity.declareORM(Type)
        Type.addActionActivate("Value", Update=ProgressBar.__updateValue)
        Type.addAction("MaxValue")
        Type.addAction("ResourceMovieProgress")
        pass

    def __init__(self):
        super(ProgressBar, self).__init__()
        pass

    def __updateValue(self, value):
        if value < 0:
            Trace.log("Entity", 0, "Incorrect value for ProgressBar %s  value- %d < 0. Remove error" % (self.object.getName(), value))
            return
            pass

        if value > self.MaxValue:
            Trace.log("Entity", 0, "Incorrect value for ProgressBar %s  value- %d > MaxValue. Remove error" % (self.object.getName(), value))
            return
            pass

        movieDuration = self.progressMovie.getDuration()

        multiply = float(self.Value) / float(self.MaxValue)

        time = movieDuration * multiply

        animation = self.progressMovie.getAnimation()
        animation.setTime(time)
        pass

    def _onInitialize(self, obj):
        super(ProgressBar, self)._onInitialize(obj)

        resource = Mengine.getResourceReference(self.ResourceMovieProgress)

        movie = self.createChild("Movie")

        movie.setName(self.ResourceMovieProgress)
        movie.setResourceMovie(resource)
        movie.enable()

        self.progressMovie = movie
        pass

    def _onPreparation(self):
        super(ProgressBar, self)._onPreparation()
        pass

    def _onActivate(self):
        super(ProgressBar, self)._onActivate()
        pass

    def _onDeactivate(self):
        super(ProgressBar, self)._onDeactivate()
        pass

    def _onFinalize(self):
        super(ProgressBar, self)._onFinalize()

        if self.progressMovie is None:
            self.progressMovie.destroy()
            self.progressMovie = None
            pass
        pass

    pass