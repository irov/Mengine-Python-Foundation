from Foundation.Task.MixinObjectTemplate import MixinMovie

from Task import Task

class TaskMovieSlotAddObject(MixinMovie, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskMovieSlotAddObject, self)._onParams(params)

        self.SlotName = params.get("SlotName")
        self.Object = params.get("Object")
        pass

    def _onRun(self):
        if self.Movie.isActive() is False:
            self.invalidTask("Movie %s not active" % (self.MovieName))
            pass

        MovieEntity = self.Movie.getEntity()

        if MovieEntity.hasMovieSlot(self.SlotName) is False:
            self.invalidTask("Movie %s not has slot %s" % (self.MovieName, self.SlotName))
            pass

        movieSlot = MovieEntity.getMovieSlot(self.SlotName)

        if self.Object.isActive() is False:
            self.invalidTask("Object %s invalid entitization" % (self.Object.getName()))
            pass

        ObjectEntity = self.Object.getEntity()

        movieSlot.addChild(ObjectEntity)

        return True
        pass
    pass