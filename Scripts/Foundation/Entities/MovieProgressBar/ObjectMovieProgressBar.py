from Foundation.Object.DemonObject import DemonObject

class ObjectMovieProgressBar(DemonObject):
    @staticmethod
    def declareORM(Type):
        DemonObject.declareORM(Type)
        Type.declareConst("ResourceMovieIdle")
        Type.declareConst("ResourceMovieOver")
        Type.declareConst("ResourceMovieBlock")
        Type.declareConst("ResourceMovieProgress")
        Type.declareConst("ResourceMovieFullProgress")
        Type.declareConst("ResourceMovieHolder")

        Type.declareParam('MaxValue')
        Type.declareParam('Value')
        Type.declareParam('Text_ID')
        Type.declareParam('Full_Text_ID')
        Type.declareParam('DoubleValue')

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