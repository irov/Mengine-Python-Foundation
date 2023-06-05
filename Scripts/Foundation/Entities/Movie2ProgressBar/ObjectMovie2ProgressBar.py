from Foundation.Object.DemonObject import DemonObject

class ObjectMovie2ProgressBar(DemonObject):
    @staticmethod
    def declareORM(Type):
        DemonObject.declareORM(Type)
        Type.addConst(Type, "ResourceMovie")
        Type.addConst(Type, "CompositionNameIdle")
        Type.addConst(Type, "CompositionNameOver")
        Type.addConst(Type, "CompositionNameBlock")
        Type.addConst(Type, "CompositionNameProgress")
        Type.addConst(Type, "CompositionNameFullProgress")
        Type.addConst(Type, "CompositionNameHolder")

        Type.addParam(Type, 'MaxValue')
        Type.addParam(Type, 'Value')
        Type.addParam(Type, 'Text_ID')
        Type.addParam(Type, 'Full_Text_ID')
        Type.addParam(Type, 'DoubleValue')
        Type.addParam(Type, 'Block')

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