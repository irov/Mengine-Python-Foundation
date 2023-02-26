from Foundation.Object.DemonObject import DemonObject

class ObjectMovieProgressBar(DemonObject):
    @staticmethod
    def declareORM(Type):
        DemonObject.declareORM(Type)
        Type.addConst(Type, "ResourceMovieIdle")
        Type.addConst(Type, "ResourceMovieOver")
        Type.addConst(Type, "ResourceMovieBlock")
        Type.addConst(Type, "ResourceMovieProgress")
        Type.addConst(Type, "ResourceMovieFullProgress")
        Type.addConst(Type, "ResourceMovieHolder")

        Type.addParam(Type, 'MaxValue')
        Type.addParam(Type, 'Value')
        Type.addParam(Type, 'Text_ID')
        Type.addParam(Type, 'Full_Text_ID')
        Type.addParam(Type, 'DoubleValue')

        pass

    def _onParams(self, params):
        super(ObjectMovieProgressBar, self)._onParams(params)
        self.initConst("ResourceMovieIdle", params, None)
        self.initConst("ResourceMovieOver", params, None)
        self.initConst("ResourceMovieProgress", params)
        self.initConst("ResourceMovieFullProgress", params, None)
        self.initConst("ResourceMovieHolder", params, None)
        self.initConst("ResourceMovieBlock", params, None)

        self.initParam('DoubleValue', params, False)
        self.initParam('Text_ID', params, 'ID_MovieProgressBar')
        self.initParam('Full_Text_ID', params, 'ID_MovieProgressBar')
        self.initParam('Value', params, 0)
        self.initParam('MaxValue', params, 100)

        pass

    pass