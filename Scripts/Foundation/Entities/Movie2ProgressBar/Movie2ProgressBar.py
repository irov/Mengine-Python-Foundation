from Foundation.Entity.BaseEntity import BaseEntity
from Foundation.ObjectManager import ObjectManager

class Movie2ProgressBar(BaseEntity):
    available_movies = ['Idle', 'Progress', 'Block', 'Idle', 'Holder']

    @staticmethod
    def declareORM(Type):
        BaseEntity.declareORM(Type)

        # EditBox
        Type.addActionActivate(Type, "DoubleValue", Update=Type._updateDoubleValue)
        Type.addActionActivate(Type, "Text_ID")
        Type.addActionActivate(Type, "Full_Text_ID")
        Type.addActionActivate(Type, "MaxValue", Update=Type._updateMaxValue)
        Type.addActionActivate(Type, "Value", Update=Type._updateValue)

        Type.addActionActivate(Type, "ResourceMovie")

        Type.addActionActivate(Type, "CompositionNameIdle")
        Type.addActionActivate(Type, "CompositionNameOver")
        Type.addActionActivate(Type, "CompositionNameBlock")
        Type.addActionActivate(Type, "CompositionNameProgress")
        Type.addActionActivate(Type, "CompositionNameFullProgress")
        Type.addActionActivate(Type, "CompositionNameHolder")
        pass

    def __init__(self):
        super(Movie2ProgressBar, self).__init__()

        self.tc = None
        self.state = "Idle"

        self.Movies = {}

        self.SemaphoreBlock = Semaphore(False, "Movie2ProgressBarBlock")
        self.time_left = 0
        pass

    def _updateDoubleValue(self, value):
        self.__choose_bar()
        pass

    def _updateValue(self, value):
        if value < 0:
            self.object.setParam('Value', 0)

        max_value = self.object.getMaxValue()

        if value > max_value:
            self.object.setParam('Value', max_value)
            return

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
        MovieProgress = self.Movies.get('Progress')

        if MovieProgress is None:
            return

        if MovieProgress.getEnable() is False:
            return

        progress = float(self.object.getValue()) / self.object.getMaxValue()
        MovieProgress.setTimingProportion(progress)

        self.__print_value()
        pass

    def clearPrintValue(self):
        text_id = self.object.getText_ID()
        movie_entity = self.Movies.get('Progress').getEntity()
        if movie_entity.hasMovieText(text_id):
            text = movie_entity.getMovieText(text_id)
            text.setTextFormatArgs(0)

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

        # full = self.object.getValue() + 0.5 >= self.object.getMaxValue()  #  it`s not clear what doing 0.5
        full = float(self.object.getValue()) >= self.object.getMaxValue()

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

    def _onInitialize(self, obj):
        super(Movie2ProgressBar, self)._onInitialize(obj)

        if self.ResourceMovie is None:
            return False
            pass

        if Menge.hasResource(self.ResourceMovie) is False:
            return False
            pass

        resource = Menge.getResourceReference(self.ResourceMovie)

        if resource is None:
            Trace.log("Entity", 0, "Movie2ProgressBar._onInitialize: not found resource %s" % (resource))
            return None
            pass

        def __createMovie2(name, comp, play, loop):
            if resource.hasComposition(comp) is False:
                return None
                pass

            mov = ObjectManager.createObjectUnique("Movie2", name, self.object, ResourceMovie=resource, CompositionName=comp)
            mov.setEnable(False)
            mov.setPlay(play)
            mov.setLoop(loop)
            mov.setInteractive(True)

            movEntityNode = mov.getEntityNode()
            self.addChild(movEntityNode)

            self.Movies[name] = mov
            return mov
            pass

        __createMovie2("Idle", self.CompositionNameIdle, True, True)
        __createMovie2("Over", self.CompositionNameOver, True, True)
        __createMovie2("Block", self.CompositionNameBlock, True, True)
        __createMovie2("Progress", self.CompositionNameProgress, False, False)
        __createMovie2("Holder", self.CompositionNameHolder, False, False)
        __createMovie2("FullProgress", self.CompositionNameFullProgress, True, True)

        idle = self.Movies.get('Idle', None)
        if idle is not None:
            idle.setEnable(True)

        progress = self.Movies.get('Progress', None)
        if progress is None:
            Trace.log("Entity", 0, "Movie2ProgressBar {} no Progress movie".format(self.getName()))
            return False

        progress.setEnable(True)
        return True

    def _onFinalize(self):
        super(Movie2ProgressBar, self)._onFinalize()

        for mov in self.Movies.itervalues():
            mov.onDestroy()
            pass

        self.Movies = {}
        pass

    def _onDeactivate(self):
        super(Movie2ProgressBar, self)._onDeactivate()

        for mov in self.Movies.itervalues():
            mov.setEnable(False)
            pass
        pass

    def _onActivate(self):
        super(Movie2ProgressBar, self)._onActivate()
        idle = self.Movies.get('Idle', None)
        if idle is not None:
            idle.setEnable(True)

        progress = self.Movies.get('Progress', None)
        if progress is not None:
            progress.setEnable(True)

        pass

    def setMovies(self, **data):
        for key, value in data.iteritems():
            if key not in Movie2ProgressBar.available_movies:
                Trace.log("Entity", 0, "Movie2ProgressBar._onInitialize: Wrong movie name %s" % (key))
                continue

            self.Movies[key] = value
        pass

    pass