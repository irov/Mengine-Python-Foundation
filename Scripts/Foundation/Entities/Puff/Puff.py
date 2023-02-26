from Foundation.Entity.BaseEntity import BaseEntity

class Puff(BaseEntity):
    @staticmethod
    def declareORM(Type):
        BaseEntity.declareORM(Type)

        Type.addAction(Type, "PuffElements")
        Type.addAction(Type, "PuffElementsVisible", Update=Puff._updatePuffElementsVisible, Append=Puff._appendPuffElementsVisible, Remove=Puff._removePuffElementsVisible)
        pass

    def _updatePuffElementsVisible(self, elementsVisible):
        for PuffElementName in self.PuffElements:
            element = self.object.getObject(PuffElementName)

            if PuffElementName in elementsVisible:
                element.setEnable(True)
            else:
                element.setEnable(False)
            pass
        pass

    def _appendPuffElementsVisible(self, id, PuffName):
        element = self.object.getObject(PuffName)

        element.setEnable(True)
        pass

    def _removePuffElementsVisible(self, id, PuffName, elements):
        element = self.object.getObject(PuffName)

        element.setEnable(False)
        pass