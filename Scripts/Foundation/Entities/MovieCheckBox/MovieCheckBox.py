from Foundation.Entity.BaseEntity import BaseEntity
from Foundation.ObjectManager import ObjectManager

from Notification import Notification

class MovieCheckBox(BaseEntity):
    @staticmethod
    def declareORM(Type):
        BaseEntity.declareORM(Type)
        Type.addActionActivate(Type, "Value", Update=MovieCheckBox.__updateValue)
        Type.addAction(Type, "ResourceMovieTrue_Idle")
        Type.addAction(Type, "ResourceMovieTrue_Enter")
        Type.addAction(Type, "ResourceMovieTrue_Over")
        Type.addAction(Type, "ResourceMovieTrue_Click")
        Type.addAction(Type, "ResourceMovieTrue_Leave")

        Type.addAction(Type, "ResourceMovieFalse_Idle")
        Type.addAction(Type, "ResourceMovieFalse_Enter")
        Type.addAction(Type, "ResourceMovieFalse_Over")
        Type.addAction(Type, "ResourceMovieFalse_Click")
        Type.addAction(Type, "ResourceMovieFalse_Leave")

        Type.addAction(Type, "BlockState")
        pass

    def __init__(self):
        super(MovieCheckBox, self).__init__()
        self.MovieButtonFalse = None
        self.MovieButtonTrue = None
        self.onClickObserver = None
        pass

    def _onInitialize(self, obj):
        super(MovieCheckBox, self)._onInitialize(obj)
        templateName = self.object.getName()
        group = self.object.getGroup()
        self.MovieButtonFalse = ObjectManager.createObjectUnique("MovieButton", templateName + "FalseButton", group, ResourceMovieIdle=self.ResourceMovieFalse_Idle, ResourceMovieEnter=self.ResourceMovieFalse_Enter, ResourceMovieOver=self.ResourceMovieFalse_Over, ResourceMovieClick=self.ResourceMovieFalse_Click, ResourceMovieLeave=self.ResourceMovieFalse_Leave)

        self.MovieButtonTrue = ObjectManager.createObjectUnique("MovieButton", templateName + "TrueButton", group, ResourceMovieIdle=self.ResourceMovieTrue_Idle, ResourceMovieEnter=self.ResourceMovieTrue_Enter, ResourceMovieOver=self.ResourceMovieTrue_Over, ResourceMovieClick=self.ResourceMovieTrue_Click, ResourceMovieLeave=self.ResourceMovieTrue_Leave)
        ent = self.MovieButtonFalse.getEntityNode()
        self.addChild(ent)
        ent2 = self.MovieButtonTrue.getEntityNode()
        self.addChild(ent2)
        pass

    def __updateValue(self, value):
        if value is True:
            self.MovieButtonFalse.setEnable(False)
            self.MovieButtonTrue.setEnable(True)
            pass
        else:
            self.MovieButtonFalse.setEnable(True)
            self.MovieButtonTrue.setEnable(False)
            pass
        pass

    def _onPreparation(self):
        super(MovieCheckBox, self)._onPreparation()
        self.MovieButtonFalse.setEnable(False)
        self.MovieButtonTrue.setEnable(False)
        pass

    def _onActivate(self):
        super(MovieCheckBox, self)._onActivate()
        self.onClickObserver = Notification.addObserver(Notificator.onMovieButtonClickEnd, self.onClick)
        pass

    def onClick(self, button):
        if self.BlockState is True:
            return False

        if button is self.MovieButtonFalse:
            self.object.setValue(True)
            Notification.notify(Notificator.onMovieCheckBox, self.object, True)
            return False
            pass
        if button is self.MovieButtonTrue:
            self.object.setValue(False)
            Notification.notify(Notificator.onMovieCheckBox, self.object, False)
            return False
            pass
        return False
        pass

    def _onDeactivate(self):
        super(MovieCheckBox, self)._onDeactivate()
        Notification.removeObserver(self.onClickObserver)
        self.onClickObserver = None
        pass

    def _onFinalize(self):
        self.MovieButtonFalse.onDestroy()
        self.MovieButtonFalse = None
        self.MovieButtonTrue.onDestroy()
        self.MovieButtonTrue = None
        pass
    pass