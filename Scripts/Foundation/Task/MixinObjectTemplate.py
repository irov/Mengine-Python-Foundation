MixinCode = '''
from Foundation.ObjectManager import ObjectManager

class {MixinType}(MixinGroup, Initializer):
    def _onParams(self, params):
        super({MixinType}, self)._onParams(params)

        self.{TypeElement} = params.get("{TypeElement}")
        self.{TypeElementName} = params.get("{TypeElementName}")
        self.{TypeElementGroup} = params.get("{TypeElementGroup}")
        self.{TypeElementGroupName} = params.get("{TypeElementGroupName}")
        pass

    def _onInitialize(self):
        super({MixinType}, self)._onInitialize()
        
        def __checkObjectType():
            TypeElements = tuple(ObjectManager.getObjectType(Type) for Type in {AliasElement})
            
            if issubclass(type(self.{TypeElement}), TypeElements) is False:
                #self.initializeFailed("Mixin {TypeElement} type '%s' is not '%s'", type(self.{TypeElement}).__name__, TypeElements)
                pass
            pass

        if self.{TypeElement} is not None:
            if _DEVELOPMENT is True:
                __checkObjectType()
                pass
                
            self.{TypeElementName} = self.{TypeElement}.getName()
            elementGroup = self.{TypeElement}.getGroup()

            if elementGroup is not None:
                self.{TypeElementGroup} = elementGroup
                self.{TypeElementGroupName} = elementGroup.getName()
                pass
            return
            pass

        if self.{TypeElementName} is None:
            self.initializeFailed("Mixin {TypeElementName} is not setup")
            pass

        if self.{TypeElementGroup} is None:
            if self.{TypeElementGroupName} is None:
                if self.Group is None:
                    self.initializeFailed("Mixin {TypeElementGroupName} %s is not setup")
                    pass

                self.{TypeElementGroup} = self.Group
                self.{TypeElementGroupName} = self.Group.getName()
                pass
            else:
                if _DEVELOPMENT is True:
                    if GroupManager.hasGroup(self.{TypeElementGroupName}) is False:
                        self.initializeFailed("Mixin {TypeElement} not found Group %s"%(self.{TypeElementGroupName}))
                        pass
                    pass

                elementGroup = GroupManager.getGroup(elementGroupName)

                self.{TypeElementGroup} = elementGroup
                self.{TypeElementGroupName} = elementGroup.getName()
                pass
            pass

        if _DEVELOPMENT is True:
            if self.{TypeElementGroup}.hasObject(self.{TypeElementName}) is False:
                self.initializeFailed("Mixin {TypeElementName} Group %s not found Object %s"%(self.{TypeElementGroupName}, self.{TypeElementName}))
                pass
            pass

        self.{TypeElement} = self.{TypeElementGroup}.getObject(self.{TypeElementName})
        
        if _DEVELOPMENT is True:
            __checkObjectType()
            pass      
        pass
    pass
'''

from Foundation.GroupManager import GroupManager
from Foundation.Initializer import Initializer
from Foundation.Task.MixinGroup import MixinGroup

def MixinObjectTemplate(TypeElement, AliasElement=None):
    MixinType = "Mixin%s" % (TypeElement)
    TypeElementName = "%sName" % (TypeElement)
    TypeElementGroup = "%sGroup" % (TypeElement)
    TypeElementGroupName = "%sGroupName" % (TypeElement)
    AliasElement = AliasElement if AliasElement is not None else (TypeElement,)

    MixinCodeElement = MixinCode.format(MixinType=MixinType, TypeElement=TypeElement, AliasElement=AliasElement, TypeElementName=TypeElementName, TypeElementGroup=TypeElementGroup, TypeElementGroupName=TypeElementGroupName)

    code = compile(MixinCodeElement, MixinType, "exec")

    MixinClass = dict(MixinGroup=MixinGroup, GroupManager=GroupManager, Initializer=Initializer)
    exec(code, MixinClass)

    return MixinClass[MixinType]
    pass

MixinHOG = MixinObjectTemplate("HOG")
MixinItem = MixinObjectTemplate("Item")
MixinSocket = MixinObjectTemplate("Socket")
MixinInteraction = MixinObjectTemplate("Interaction")
MixinShift = MixinObjectTemplate("Shift")
MixinPuff = MixinObjectTemplate("Puff")
MixinZoom = MixinObjectTemplate("Zoom")
MixinDialog = MixinObjectTemplate("Dialog")
MixinCutZoom = MixinObjectTemplate("CutZoom")
MixinMovie = MixinObjectTemplate("Movie")
MixinMovie2 = MixinObjectTemplate("Movie2")
MixinPoint = MixinObjectTemplate("Point")
MixinButton = MixinObjectTemplate("Button")
MixinAnimation = MixinObjectTemplate("Animation")
MixinTransition = MixinObjectTemplate("Transition")
MixinFan = MixinObjectTemplate("Fan")
MixinFanItem = MixinObjectTemplate("FanItem")
MixinCheckBox = MixinObjectTemplate("CheckBox")
MixinMovieCheckBox = MixinObjectTemplate("MovieCheckBox")
MixinMovie2CheckBox = MixinObjectTemplate("Movie2CheckBox")
MixinCheckBoxAlias = MixinObjectTemplate("CheckBox", ("CheckBox", "MovieCheckBox", "Movie2CheckBox"))
MixinVideo = MixinObjectTemplate("Video")
MixinText = MixinObjectTemplate("Text")
MixinStates = MixinObjectTemplate("States")
MixinInventoryItem = MixinObjectTemplate("InventoryItem")
MixinMovieButton = MixinObjectTemplate("MovieButton")
MixinMovie2Button = MixinObjectTemplate("Movie2Button")
MixinMovieItem = MixinObjectTemplate("MovieItem")