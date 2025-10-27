from Foundation.Object.DemonObject import DemonObject

class ObjectMovie2ProgressBar(DemonObject):
    @staticmethod
    def declareORM(Type):
        DemonObject.declareORM(Type)
        Type.declareConst("ResourceMovie")
        Type.declareConst("CompositionNameIdle")
        Type.declareConst("CompositionNameOver")
        Type.declareConst("CompositionNameBlock")
        Type.declareConst("CompositionNameProgress")
        Type.declareConst("CompositionNameFullProgress")
        Type.declareConst("CompositionNameHolder")

        Type.declareParam('MaxValue')
        Type.declareParam('Value')
        Type.declareParam('Text_ID')
        Type.declareParam('Full_Text_ID')
        Type.declareParam('DoubleValue')
        Type.declareParam('Block')
        pass

    def _onParams(self, params):
        super(ObjectMovie2ProgressBar, self)._onParams(params)
        self.initConst("ResourceMovie", params, None)

        self.initConst("CompositionNameIdle", params, None)
        self.initConst("CompositionNameOver", params, None)
        self.initConst("CompositionNameProgress", params)
        self.initConst("CompositionNameFullProgress", params, None)
        self.initConst("CompositionNameHolder", params, None)
        self.initConst("CompositionNameBlock", params, None)

        self.initParam('DoubleValue', params, False)
        self.initParam('Text_ID', params, 'ID_MovieProgressBar')
        self.initParam('Full_Text_ID', params, 'ID_MovieProgressBar')
        self.initParam('Value', params, 0)
        self.initParam('MaxValue', params, 100)
        self.initParam('Block', params, False)

    def eachMovies(self):
        if self.isActive() is not False:
            Entity = self.getEntity()

            for Movie in Entity.Movies.itervalues():
                yield Movie

    def setTextAliasEnvironment(self, env_name):
        for movie in self.eachMovies():
            movie.setTextAliasEnvironment(env_name)