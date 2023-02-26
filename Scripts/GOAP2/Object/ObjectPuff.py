from Object import Object

class ObjectPuff(Object):
    @staticmethod
    def declareORM(Type):
        Object.declareORM(Type)

        Type.addParam(Type, "PuffElements")
        Type.addParam(Type, "PuffElementsVisible")
        pass

    def _onParams(self, params):
        super(ObjectPuff, self)._onParams(params)
        self.initParam("PuffElements", params, [])
        self.initParam("PuffElementsVisible", params, [])
        pass

    def _onLoader(self):
        super(ObjectPuff, self)._onLoader()

        PuffElements = self.getObjects()

        for PuffElement in PuffElements:
            PuffElement.setEnable(False)
            pass

        self.params["PuffElements"] = [PuffElement.getName() for PuffElement in PuffElements]
        pass

    def hasElement(self, name):
        return name in self.params["PuffElements"]
        pass

    def addVisibleElement(self, elementName):
        PuffElementsVisible = self.getPuffElementsVisible()

        if elementName in PuffElementsVisible:
            return

        self.appendParam("PuffElementsVisible", elementName)
        pass

    def removeVisibleElement(self, elementName):
        PuffElementsVisible = self.getPuffElementsVisible()

        if elementName not in PuffElementsVisible:
            return

        self.delParam("PuffElementsVisible", elementName)
        pass
    pass