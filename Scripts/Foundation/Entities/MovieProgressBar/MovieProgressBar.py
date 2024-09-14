from Foundation.Entity.BaseEntity import BaseEntity
from Foundation.ObjectManager import ObjectManager

class MovieProgressBar(BaseEntity):
    available_movies = ['Idle', 'Progress', 'Block', 'Idle', 'Holder']

    @staticmethod
    def declareORM(Type):
        BaseEntity.declareORM(Type)

        Type.addActionActivate(Type, "DoubleValue", Update=Type._updateDoubleValue)
        Type.addActionActivate(Type, "Text_ID")
        Type.addActionActivate(Type, "Full_Text_ID")
        Type.addActionActivate(Type, "MaxValue", Update=Type._updateMaxValue)
        Type.addActionActivate(Type, "Value", Update=Type._updateValue)

        Type.addActionActivate(Type, "ResourceMovieIdle")
        Type.addActionActivate(Type, "ResourceMovieOver")
        Type.addActionActivate(Type, "ResourceMovieBlock")
        Type.addActionActivate(Type, "ResourceMovieProgress")
        Type.addActionActivate(Type, "ResourceMovieFullProgress")
        Type.addActionActivate(Type, "ResourceMovieHolder")
        pass

    def _updateDoubleValue(self, value):
        self.__choose_bar()
        pass

    def _updateValue(self, value):
        if value < 0:
            self.object.setParam('Value', 0)

        # max_value = self.object.getMaxValue()
        #
        # if value > max_value:
        #     self.object.setParam('Value', max_value)
        #     return

        self.__choose_bar()
        pass

    def _updateMaxValue(self, value):
        if value < 0:
            self.object.setParam('MaxValue', 0)

        # cur_value = self.object.getValue()
        #
        # if value < cur_value:
        #     self.object.setParam('MaxValue', cur_value)
        #     return

        self.__choose_bar()
        pass

    def get_progress(self):
        return float(self.object.getValue()) / self.object.getMaxValue()

    def __place_progress(self):
        if self.Movies.get('Progress', None) is None:
            return

        progress = float(self.object.getValue()) / self.object.getMaxValue()
        self.Movies.get('Progress').setTimingProportion(progress)

        self.__print_value()
        pass

    def __print_value(self):
        text_id = self.object.getText_ID()
        if text_id is None:
            return
        movie_entity = self.Movies.get('Progress').getEntity()

        if movie_entity.hasMovieText(text_id):
            text = movie_entity.getMovieText(text_id)
            if self.object.getDoubleValue() is False:
                text.setTextFormatArgs(int(self.object.getValue() + 0.5))
            else:
                text.setTextFormatArgs(int(self.object.getValue() + 0.5), int(self.object.getMaxValue() + 0.5))
            pass
        pass

    def __choose_bar(self):
        if self.Movies.get('FullProgress', None) is None:
            self.__place_progress()
            return

        full = self.object.getValue() + 0.5 >= self.object.getMaxValue()
        self.Movies['Progress'].setEnable(not full)
        self.Movies['FullProgress'].setEnable(full)

        self.__print_full_value()
        self.__place_progress()
        pass

    def __print_full_value(self):
        text_id = self.object.getFull_Text_ID()
        if text_id is None:
            return
        movie_entity = self.Movies.get('FullProgress').getEntity()

        if movie_entity.hasMovieText(text_id):
            text = movie_entity.getMovieText(text_id)
            if self.object.getDoubleValue() is False:
                text.setTextFormatArgs(int(self.object.getValue() + 0.5))
            else:
                text.setTextFormatArgs(int(self.object.getValue() + 0.5), int(self.object.getMaxValue() + 0.5))
            pass
        pass

    def set_progress(self, progress):
        if progress > 1:
            progress = 1

        new_value = int(progress * self.object.getMaxValue())
        self.object.setParam('Value', new_value)
        pass

    def __init__(self):
        super(MovieProgressBar, self).__init__()

        self.tc = None
        self.state = "Idle"

        self.Movies = {}

        self.SemaphoreBlock = Semaphore(False, "MovieProgressBarBlock")
        self.time_left = 0
        pass

    def _onInitialize(self, obj):
        super(MovieProgressBar, self)._onInitialize(obj)

        def __createMovie(name, res, play, loop):
            if res is None:
                return None
                pass

            if Mengine.hasResource(res) is False:
                return False
                pass

            resource = Mengine.getResourceReference(res)

            if resource is None:
                Trace.log("Entity", 0, "MovieProgressBar._onInitialize: not found resource %s" % (res))
                return None
                pass

            mov = ObjectManager.createObjectUnique("Movie", name, self.object, ResourceMovie=resource)
            mov.setEnable(False)
            mov.setPlay(play)
            mov.setLoop(loop)

            movEntityNode = mov.getEntityNode()
            self.addChild(movEntityNode)

            self.Movies[name] = mov
            return mov
            pass

        __createMovie("Idle", self.ResourceMovieIdle, True, True)
        __createMovie("Over", self.ResourceMovieOver, True, True)
        __createMovie("Block", self.ResourceMovieBlock, True, True)
        __createMovie("Progress", self.ResourceMovieProgress, False, False)
        __createMovie("Holder", self.ResourceMovieHolder, False, False)
        __createMovie("FullProgress", self.ResourceMovieFullProgress, True, True)
        idle = self.Movies.get('Idle', None)
        if idle is not None:
            idle.setEnable(True)
        self.Movies['Progress'].setEnable(True)

        self.scheduler = Mengine.createScheduler()
        return True

    def increase_smoothly_value(self, source, value, time, func=None, smooth_delta=50.0):
        times = time / smooth_delta
        delta_value = value / times

        self.time_left = time

        def _pipe(index, self):
            self.time_left -= smooth_delta
            if self.time_left > 0:
                return smooth_delta
            return -1

        def _update(index, delay, self):
            old_value = self.object.getValue()
            self.object.setValue(old_value + delta_value)
            if func is not None and int(old_value + delta_value + 0.5) - int(old_value + 0.5) > 0:
                func()
            pass

        source.addTask("TaskPipe", Scheduler=self.scheduler, Pipe=_pipe, Update=_update, Args=(self,))
        pass

    def _onFinalize(self):
        super(MovieProgressBar, self)._onFinalize()

        for mov in self.Movies.itervalues():
            mov.onDestroy()
            pass

        self.Movies = {}

        if self.scheduler is not None:
            Mengine.destroyScheduler(self.scheduler)
            self.scheduler = None
        pass

    def _onDeactivate(self):
        super(MovieProgressBar, self)._onDeactivate()

        for mov in self.Movies.itervalues():
            mov.setEnable(False)
            pass
        pass

    def _onActivate(self):
        super(MovieProgressBar, self)._onActivate()
        idle = self.Movies.get('Idle', None)
        if idle is not None:
            idle.setEnable(True)
        self.Movies['Progress'].setEnable(True)
        pass

    def setMovies(self, **data):
        for key, value in data.iteritems():
            if key not in MovieProgressBar.available_movies:
                Trace.log("Entity", 0, "MovieProgressBar._onInitialize: Wrong movie name %s" % (key))
                continue

            self.Movies[key] = value
        pass

    pass