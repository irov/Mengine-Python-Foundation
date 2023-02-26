from GOAP2.Task.MixinObjectTemplate import MixinMovie

from Task import Task

class TaskMovieSlotAddChild(MixinMovie, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskMovieSlotAddChild, self)._onParams(params)

        self.SlotName = params.get("SlotName")
        self.Node = params.get("Node")
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

        movieSlot.addChild(self.Node)

        return True
        pass
    pass