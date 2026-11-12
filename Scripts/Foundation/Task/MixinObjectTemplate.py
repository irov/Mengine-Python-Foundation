from Foundation.GroupManager import GroupManager
from Foundation.Initializer import Initializer
from Foundation.Task.MixinGroup import MixinGroup
from Foundation.ObjectManager import ObjectManager


@meta.template
def MixinObjectTemplate(TypeElement, AliasElement=None, MixinType=None):
    if MixinType is None:
        MixinType = @meta.concat("Mixin", TypeElement)

    TypeElementName = @meta.concat(TypeElement, "Name")
    TypeElementGroup = @meta.concat(TypeElement, "Group")
    TypeElementGroupName = @meta.concat(TypeElement, "GroupName")
    if AliasElement is None:
        AliasElement = (TypeElement,)

    @meta.emit(name=MixinType)
    class Generated(MixinGroup, Initializer):
        def _onParams(self, params):
            super(@meta.current_class(), self)._onParams(params)

            @meta.setattr(self, TypeElement, params.get(TypeElement))
            @meta.setattr(self, TypeElementName, params.get(TypeElementName))
            @meta.setattr(self, TypeElementGroup, params.get(TypeElementGroup))
            @meta.setattr(self, TypeElementGroupName, params.get(TypeElementGroupName))
            pass

        def _onInitialize(self):
            super(@meta.current_class(), self)._onInitialize()

            def __checkObjectType():
                TypeElements = tuple(ObjectManager.getObjectType(Type) for Type in AliasElement)

                if issubclass(type(@meta.getattr(self, TypeElement)), TypeElements) is False:
                    # self.initializeFailed("Mixin object has an unexpected type")
                    pass
                pass

            if @meta.getattr(self, TypeElement) is not None:
                if _DEVELOPMENT is True:
                    __checkObjectType()
                    pass

                @meta.setattr(self, TypeElementName, @meta.getattr(self, TypeElement).getName())
                elementGroup = @meta.getattr(self, TypeElement).getGroup()

                if elementGroup is not None:
                    @meta.setattr(self, TypeElementGroup, elementGroup)
                    @meta.setattr(self, TypeElementGroupName, elementGroup.getName())
                    pass
                return

            if @meta.getattr(self, TypeElementName) is None:
                self.initializeFailed(@meta.concat("Mixin ", TypeElementName, " is not setup"))
                pass

            if @meta.getattr(self, TypeElementGroup) is None:
                if @meta.getattr(self, TypeElementGroupName) is None:
                    if self.Group is None:
                        self.initializeFailed(@meta.concat("Mixin ", TypeElementGroupName, " %s is not setup"))
                        pass

                    @meta.setattr(self, TypeElementGroup, self.Group)
                    @meta.setattr(self, TypeElementGroupName, self.Group.getName())
                    pass
                else:
                    if _DEVELOPMENT is True:
                        if GroupManager.hasGroup(@meta.getattr(self, TypeElementGroupName)) is False:
                            self.initializeFailed(@meta.concat("Mixin ", TypeElement, " not found Group %s") % (@meta.getattr(self, TypeElementGroupName)))
                            pass
                        pass

                    elementGroup = GroupManager.getGroup(@meta.getattr(self, TypeElementGroupName))

                    @meta.setattr(self, TypeElementGroup, elementGroup)
                    @meta.setattr(self, TypeElementGroupName, elementGroup.getName())
                    pass
                pass

            if _DEVELOPMENT is True:
                if @meta.getattr(self, TypeElementGroup).hasObject(@meta.getattr(self, TypeElementName)) is False:
                    self.initializeFailed(@meta.concat("Mixin ", TypeElementName, " Group %s not found Object %s") % (@meta.getattr(self, TypeElementGroupName), @meta.getattr(self, TypeElementName)))
                    pass
                pass

            @meta.setattr(self, TypeElement, @meta.getattr(self, TypeElementGroup).getObject(@meta.getattr(self, TypeElementName)))

            if _DEVELOPMENT is True:
                __checkObjectType()
                pass
            pass
        pass


MixinHOG = @meta.expand(MixinObjectTemplate, "HOG")
MixinItem = @meta.expand(MixinObjectTemplate, "Item")
MixinSocket = @meta.expand(MixinObjectTemplate, "Socket")
MixinInteraction = @meta.expand(MixinObjectTemplate, "Interaction")
MixinShift = @meta.expand(MixinObjectTemplate, "Shift")
MixinPuff = @meta.expand(MixinObjectTemplate, "Puff")
MixinZoom = @meta.expand(MixinObjectTemplate, "Zoom")
MixinDialog = @meta.expand(MixinObjectTemplate, "Dialog")
MixinCutZoom = @meta.expand(MixinObjectTemplate, "CutZoom")
MixinMovie = @meta.expand(MixinObjectTemplate, "Movie")
MixinMovie2 = @meta.expand(MixinObjectTemplate, "Movie2")
MixinPoint = @meta.expand(MixinObjectTemplate, "Point")
MixinButton = @meta.expand(MixinObjectTemplate, "Button")
MixinAnimation = @meta.expand(MixinObjectTemplate, "Animation")
MixinTransition = @meta.expand(MixinObjectTemplate, "Transition")
MixinFan = @meta.expand(MixinObjectTemplate, "Fan")
MixinFanItem = @meta.expand(MixinObjectTemplate, "FanItem")
MixinCheckBox = @meta.expand(MixinObjectTemplate, "CheckBox")
MixinMovieCheckBox = @meta.expand(MixinObjectTemplate, "MovieCheckBox")
MixinMovie2CheckBox = @meta.expand(MixinObjectTemplate, "Movie2CheckBox")
MixinCheckBoxAlias = @meta.expand(MixinObjectTemplate, "CheckBox", ("CheckBox", "MovieCheckBox", "Movie2CheckBox"), MixinType="MixinCheckBoxAlias")
MixinVideo = @meta.expand(MixinObjectTemplate, "Video")
MixinText = @meta.expand(MixinObjectTemplate, "Text")
MixinStates = @meta.expand(MixinObjectTemplate, "States")
MixinInventoryItem = @meta.expand(MixinObjectTemplate, "InventoryItem")
MixinMovieButton = @meta.expand(MixinObjectTemplate, "MovieButton")
MixinMovie2Button = @meta.expand(MixinObjectTemplate, "Movie2Button")
MixinMovieItem = @meta.expand(MixinObjectTemplate, "MovieItem")