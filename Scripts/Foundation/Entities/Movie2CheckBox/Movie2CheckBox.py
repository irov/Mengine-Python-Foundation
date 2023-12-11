from Foundation.Entity.BaseEntity import BaseEntity

from Foundation.ObjectManager import ObjectManager
from Foundation.TaskManager import TaskManager


class Movie2CheckBox(BaseEntity):

    @staticmethod
    def declareORM(Type):
        BaseEntity.declareORM(Type)
        Type.addActionActivate(Type, "Value", Update=Movie2CheckBox.__updateValue)

        Type.addAction(Type, "ResourceMovie")

        Type.addAction(Type, "CompositionNameTrue_Idle")
        Type.addAction(Type, "CompositionNameTrue_Enter")
        Type.addAction(Type, "CompositionNameTrue_Over")
        Type.addAction(Type, "CompositionNameTrue_Click")
        Type.addAction(Type, "CompositionNameTrue_Leave")

        Type.addAction(Type, "CompositionNameFalse_Idle")
        Type.addAction(Type, "CompositionNameFalse_Enter")
        Type.addAction(Type, "CompositionNameFalse_Over")
        Type.addAction(Type, "CompositionNameFalse_Click")
        Type.addAction(Type, "CompositionNameFalse_Leave")

        Type.addAction(Type, "BlockState")

    def __init__(self):
        super(Movie2CheckBox, self).__init__()
        self.tc = None

        self.MovieButtonFalse = None
        self.MovieButtonTrue = None

    def _onInitialize(self, obj):
        super(Movie2CheckBox, self)._onInitialize(obj)

        check_box_name = self.object.getName()
        group = self.object.getGroup()

        self.MovieButtonFalse = ObjectManager.createObjectUnique("Movie2Button", check_box_name + "FalseButton",
                                                                 group, ResourceMovie=self.ResourceMovie,
                                                                 CompositionNameIdle=self.CompositionNameFalse_Idle,
                                                                 CompositionNameEnter=self.CompositionNameFalse_Enter,
                                                                 CompositionNameOver=self.CompositionNameFalse_Over,
                                                                 CompositionNameClick=self.CompositionNameFalse_Click,
                                                                 CompositionNameLeave=self.CompositionNameFalse_Leave)

        self.MovieButtonTrue = ObjectManager.createObjectUnique("Movie2Button", check_box_name + "TrueButton", group,
                                                                ResourceMovie=self.ResourceMovie,
                                                                CompositionNameIdle=self.CompositionNameTrue_Idle,
                                                                CompositionNameEnter=self.CompositionNameTrue_Enter,
                                                                CompositionNameOver=self.CompositionNameTrue_Over,
                                                                CompositionNameClick=self.CompositionNameTrue_Click,
                                                                CompositionNameLeave=self.CompositionNameTrue_Leave)

        button_false_entity_node = self.MovieButtonFalse.getEntityNode()
        self.addChild(button_false_entity_node)

        button_true_entity_node = self.MovieButtonTrue.getEntityNode()
        self.addChild(button_true_entity_node)

    def setBlock(self, value):
        self.MovieButtonFalse.setBlock(value)
        self.MovieButtonTrue.setBlock(value)

    def __updateValue(self, value):
        if value is True:
            self.MovieButtonFalse.setEnable(False)
            self.MovieButtonTrue.setEnable(True)
        else:
            self.MovieButtonFalse.setEnable(True)
            self.MovieButtonTrue.setEnable(False)

    def _onPreparation(self):
        super(Movie2CheckBox, self)._onPreparation()

        self.MovieButtonFalse.setEnable(False)
        self.MovieButtonTrue.setEnable(False)

    def __resolveClick(self, holder):
        if self.BlockState is True:
            return

        button = holder.get()

        if button is self.MovieButtonFalse:
            self.object.setValue(True)
            Notification.notify(Notificator.onMovie2CheckBox, self.object, True)
        elif button is self.MovieButtonTrue:
            self.object.setValue(False)
            Notification.notify(Notificator.onMovie2CheckBox, self.object, False)

    def _onActivate(self):
        super(Movie2CheckBox, self)._onActivate()

        click_holder = Holder()
        self.tc = TaskManager.createTaskChain(Repeat=True)

        with self.tc as source:
            with source.addRaceTask(2) as (source_btn_true, source_btn_false):
                # source_btn_true.addTask("TaskMovie2ButtonClick", Movie2Button=self.MovieButtonTrue)
                source_btn_true.addListener(Notificator.onMovie2ButtonClickEnd, lambda mb: mb is self.MovieButtonTrue)
                source_btn_true.addFunction(click_holder.set, self.MovieButtonTrue)

                # source_btn_false.addTask("TaskMovie2ButtonClick", Movie2Button=self.MovieButtonFalse)
                source_btn_false.addListener(Notificator.onMovie2ButtonClickEnd, lambda mb: mb is self.MovieButtonFalse)
                source_btn_false.addFunction(click_holder.set, self.MovieButtonFalse)

            source.addFunction(self.__resolveClick, click_holder)

    def _onDeactivate(self):
        super(Movie2CheckBox, self)._onDeactivate()

        if self.tc is not None:
            self.tc.cancel()
            self.tc = None

    def _onFinalize(self):
        super(Movie2CheckBox, self)._onFinalize()

        if self.MovieButtonFalse is not None:
            self.MovieButtonFalse.onDestroy()
            self.MovieButtonFalse = None

        if self.MovieButtonTrue is not None:
            self.MovieButtonTrue.onDestroy()
            self.MovieButtonTrue = None

    def getCurrentMovie(self):
        if self.Value is True:
            return self.MovieButtonTrue
        else:
            return self.MovieButtonFalse

    def getCompositionBounds(self):
        current_movie = self.getCurrentMovie()
        return current_movie.getCompositionBounds()

    def hasCompositionBounds(self):
        current_movie = self.getCurrentMovie()
        return current_movie.hasCompositionBounds()
