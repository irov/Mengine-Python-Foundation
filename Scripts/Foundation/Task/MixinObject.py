from Foundation.Initializer import Initializer
from Foundation.Object.BaseObject import BaseObject
from Foundation.Task.MixinGroup import MixinGroup

class MixinObject(MixinGroup, Initializer):
    __metaclass__ = baseslots("Object", "ObjectName")

    def _onParams(self, params):
        super(MixinObject, self)._onParams(params)

        self.Object = params.get("Object")
        self.ObjectName = params.get("ObjectName")
        pass

    def _onInitialize(self):
        super(MixinObject, self)._onInitialize()

        if self.Object is not None:
            if isinstance(self.Object, BaseObject) is True:
                self.ObjectName = self.Object.getName()
                return

            if isinstance(self.Object, str) is True:
                self.ObjectName = self.Object
                self.Object = None
            else:
                self.initializeFailed("Mixin MixinObject Object is not BaseObject or str")
                pass
            pass

        if _DEVELOPMENT is True:
            if self.ObjectName is None:
                self.initializeFailed("Mixin MixinObject ObjectName setup is None")
                pass

            if self.Group is None:
                self.initializeFailed("Mixin MixinObject Group is not setup")
                pass

            if self.Group.hasObject(self.ObjectName) is False:
                groupName = self.Group.getName()

                self.initializeFailed("Mixin MixinObject Group %s not found Object %s" % (groupName, self.ObjectName))
                pass
            pass

        self.Object = self.Group.getObject(self.ObjectName)
        pass
    pass