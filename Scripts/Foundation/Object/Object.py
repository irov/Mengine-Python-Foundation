from Foundation.Object.EntityObject import EntityObject

class Object(EntityObject):
    def isSavable(self):
        return False
        pass

    def _onSave(self):
        return None
        pass

    def _onLoad(self, load_obj):
        pass

    def _paramsFailed(self, msg):
        return "Object %s group '%s' name '%s' %s" % (self, self.getGroupName(), self.getName(), msg)
        pass
    pass