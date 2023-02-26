from Foundation.Object.ChildObject import ChildObject
from Foundation.Object.EntityObject import EntityObject

class DemonObject(ChildObject, EntityObject):
    def __init__(self):
        super(DemonObject, self).__init__()
        pass

    def isSavable(self):
        return False
        pass

    def _onSave(self):
        return None
        pass

    def _onLoad(self, load_obj):
        pass

    def _paramsFailed(self, msg):
        return "DemonObject [%s] group '%s' name '%s' %s" % (self, self.getGroupName(), self.getName(), msg)
        pass

    def _onActivate(self):
        entity = self.initializeEntity()

        if entity is None:
            Trace.log("Object", 0, "DemonObject %s invalid activate" % (self.getName()))

            return False
            pass

        objects = self.getObjects()

        for obj in objects:
            obj.onActivate()

            obj_entity = obj.getEntityNode()
            obj_entity.disable()

            entity.addChild(obj_entity)
            pass
        pass

    def _onDeactivate(self):
        super(DemonObject, self)._onDeactivate()
        pass

    def _onFinalize(self):
        super(DemonObject, self)._onFinalize()
        pass

    def onEntityRestore(self):
        if self.isActive() is False:
            return
            pass

        objects = self.getObjects()

        for obj in objects:
            obj.onEntityRestore()
            pass

        self.entity.onRestore()
        pass
    pass