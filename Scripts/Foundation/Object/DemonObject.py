from Foundation.Object.ChildObject import ChildObject
from Foundation.Object.EntityObject import EntityObject


class DemonObject(ChildObject, EntityObject):
    def __init__(self):
        super(DemonObject, self).__init__()
        pass

    def isSavable(self):
        return False

    def _onSave(self):
        return None

    def _onLoad(self, load_obj):
        pass

    def _paramsFailed(self, msg):
        return "DemonObject [%s] group '%s' name '%s' %s" % (self, self.getGroupName(), self.getName(), msg)

    def _onActivate(self):
        entity = self.initializeEntity()

        if entity is None:
            Trace.log("Object", 0, "DemonObject %s invalid activate" % (self.getName()))

            return False

        objects = self.getObjects()

        for obj in objects:
            obj.onActivate()

            obj_entity = obj.getEntityNode()
            obj_entity.disable()

            entity.addChild(obj_entity)

    def _onDeactivate(self):
        super(DemonObject, self)._onDeactivate()

    def _onFinalize(self):
        super(DemonObject, self)._onFinalize()

    def onEntityRestore(self):
        if self.isActive() is False:
            return

        objects = self.getObjects()

        for obj in objects:
            obj.onEntityRestore()

        self.entity.onRestore()