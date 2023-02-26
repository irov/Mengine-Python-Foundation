from GOAP2.Task.MixinObjectTemplate import MixinMovie
from GOAP2.Task.MixinObserver import MixinObserver
from GOAP2.Task.Task import Task

class TaskMovieSocketEnable(MixinMovie, MixinObserver, Task):
    def _onParams(self, params):
        super(TaskMovieSocketEnable, self)._onParams(params)

        self.SocketName = params.get("SocketName")
        self.Value = params.get("Value", True)
        pass

    def _onInitialize(self):
        super(TaskMovieSocketEnable, self)._onInitialize()
        if _DEVELOPMENT is True:
            ResourceMovie = self.Movie.getResourceMovie()
            hasSocket = Menge.hasMovieSocket(ResourceMovie, self.SocketName)
            if hasSocket is False:
                return False
                pass
            pass

        return True
        pass

    def _onRun(self):
        MovieEntity = self.Movie.getEntity()
        socket = MovieEntity.getSocket(self.SocketName)

        if self.Value is False:
            socket.disable()
            pass
        else:
            socket.enable()
            pass

        return True
        pass

    pass