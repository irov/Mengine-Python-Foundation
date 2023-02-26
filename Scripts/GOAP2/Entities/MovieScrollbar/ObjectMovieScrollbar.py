from GOAP2.Object.DemonObject import DemonObject

class ObjectMovieScrollbar(DemonObject):

    @staticmethod
    def declareORM(Type):
        DemonObject.declareORM(Type)
        Type.addConst(Type, 'ResourceMovieSlider')
        Type.addConst(Type, 'ResourceMovieBar')
        Type.addConst(Type, 'IsHorizontal')
        Type.addParam(Type, 'setToZero')
        Type.addParam(Type, 'Value')

    def __init__(self):
        super(ObjectMovieScrollbar, self).__init__()

        self.onScroll = Event('onScroll')
        self.onScrollEnd = Event('onScrollEnd')
        self.onScrollStart = Event('onScrollStart')

    def _onParams(self, params):
        super(ObjectMovieScrollbar, self)._onParams(params)
        self.initConst('ResourceMovieSlider', params, None)
        self.initConst('ResourceMovieBar', params, None)
        self.initConst('IsHorizontal', params, False)
        self.initParam('setToZero', params, True)
        self.initParam('Value', params, 0.0)