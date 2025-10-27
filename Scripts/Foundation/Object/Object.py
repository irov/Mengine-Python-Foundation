from Foundation.Object.EntityObject import EntityObject

class Object(EntityObject):
    @staticmethod
    def declareORM(Type):
        EntityObject.declareORM(Type)
        pass

    def isSavable(self):
        return False

    def _onSave(self):
        return None

    def _onLoad(self, load_obj):
        pass

    def _paramsFailed(self, msg):
        return "Object %s group '%s' name '%s' %s" % (self, self.getGroupName(), self.getName(), msg)
    pass