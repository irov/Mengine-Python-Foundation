from math import fabs

from Foundation.Task.MixinObjectTemplate import MixinMovie
from Foundation.Task.Semaphore import Semaphore
from Foundation.Task.TaskAlias import TaskAlias

class TaskMovieSocketSwipe(TaskAlias, MixinMovie):
    def _onParams(self, params):
        super(TaskMovieSocketSwipe, self)._onParams(params)
        self.SocketName = params.get("SocketName")
        self.Direction = params.get("Direction")
        self.catchTry = params.get("catchTry", False)
        self.delay = params.get("Delay", 1000)
        pass

    def _onInitialize(self):
        super(TaskMovieSocketSwipe, self)._onInitialize()

        if _DEVELOPMENT is True:
            if self.SocketName is None:
                self.initializeFailed("SocketName is None")
                pass

            if self.Direction not in ["Up", "Down", "Left", "Right"]:
                self.initializeFailed("Direction is incorrect")
                pass
            pass

        self.MoveAdapter = None
        self.ButtonAdapter = None
        self.sem_remove = Semaphore(0, "remove")
        self.sem_complete = Semaphore(0, "complete")
        self.min_distance = 100.0
        self.min_swipe_distance = 400.0
        self.current_distance = 0.0
        self.startXY = None
        self.dir = None
        self.dxy = None
        pass

    def _onGenerate(self, source):
        if self.Movie.getEnable() is False:
            self.invalidTask("Movie %s is Disable" % (self.Movie.getName()))
            pass

        EntityNode = self.Movie.getEntityNode()

        if EntityNode is None:
            self.validateFailed("Movie %s is not Active" % (self.Movie.getName()))
            pass

        if Mengine.isHomeless(EntityNode) is True:
            self.invalidTask("Movie %s is Homeless" % (self.Movie.getName()))
            pass

        def __detector(isSkip, cb):
            def __mouseMove(event):
                x = event.x
                y = event.y
                if self.startXY is None:
                    self.startXY = (x, y)

                self.current_distance = pow(pow(x - self.startXY[0], 2) + pow(y - self.startXY[1], 2), 0.5)
                self.dxy = (x - self.startXY[0], y - self.startXY[1])
                if fabs(self.dxy[1]) - fabs(self.dxy[0]) > 0:  # up or down
                    if -0.27 <= float(self.dxy[0] / self.dxy[1]) <= 0.27:
                        if self.dxy[1] > 0:
                            self.dir = "Down"
                        else:
                            self.dir = "Up"
                        pass
                    pass

                if fabs(self.dxy[1]) - fabs(self.dxy[0]) < 0:  # left or right
                    if -0.27 <= float(self.dxy[1] / self.dxy[0]) <= 0.27:
                        if self.dxy[0] > 0:
                            self.dir = "Right"
                        else:
                            self.dir = "Left"
                        pass
                    pass
                pass

            def __mouseClick(event, isSkip, cb):
                if event.isDown is True:
                    return

                if self.dir != self.Direction:
                    cb(isSkip, 0)  # no swipe

                elif 0 <= self.current_distance <= self.min_distance:
                    cb(isSkip, 0)  # no swipe
                elif self.min_distance < self.current_distance < self.min_swipe_distance:
                    cb(isSkip, 1)  # try swipe
                elif self.min_swipe_distance <= self.current_distance:
                    cb(isSkip, 2)  # swipe
                else:
                    cb(isSkip, 0)

                __removeHandlers()
                pass

            if cb is None:
                __removeHandlers()
            else:
                self.MoveAdapter = Mengine.addMouseMoveHandler(__mouseMove)
                self.ButtonAdapter = Mengine.addMouseButtonHandler(__mouseClick, isSkip, cb)
            pass

        def __removeHandlers():
            if self.MoveAdapter is not None:
                Mengine.removeGlobalHandler(self.MoveAdapter)
            if self.ButtonAdapter is not None:
                Mengine.removeGlobalHandler(self.ButtonAdapter)
            self.MoveAdapter = None
            self.ButtonAdapter = None
            self.current_distance = 0.0
            self.startXY = None
            self.dir = None
            self.dxy = None
            pass

        with source.addRepeatTask() as (repeat, until):
            with repeat.addIfTask(self.Movie.getEnable) as (enabled, disabled):
                enabled.addTask("TaskDummy")
                disabled.addTask("TaskDeadLock")
                pass

            repeat.addTask("TaskMovieSocketClick", SocketName=self.SocketName, Movie=self.Movie, isDown=True)
            with repeat.addRaceTask(2) as (handlers, timer):
                handlers.addTask("TaskSemaphore", Semaphore=self.sem_remove, To=1)
                with handlers.addSwitchTask(3, __detector) as (no_swipe, try_swipe, swipe):
                    try_swipe.addTask("TaskSemaphore", Semaphore=self.sem_complete, To=2)
                    swipe.addTask("TaskSemaphore", Semaphore=self.sem_complete, To=1)
                    pass
                handlers.addTask("TaskSemaphore", Semaphore=self.sem_remove, To=0)

                timer.addDelay(self.delay)
                pass

            with repeat.addIfTask(lambda: self.sem_remove.getValue() == 1) as (remove, not_remove):
                remove.addFunction(__removeHandlers)
                remove.addTask("TaskSemaphore", Semaphore=self.sem_remove, To=0)

            if self.catchTry is True:
                until.addTask("TaskSemaphore", Semaphore=self.sem_complete, From=2)
            else:
                until.addTask("TaskSemaphore", Semaphore=self.sem_complete, From=1)
            pass
        pass
    pass