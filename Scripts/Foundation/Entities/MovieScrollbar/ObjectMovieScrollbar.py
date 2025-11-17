from Foundation.Object.DemonObject import DemonObject

class ObjectMovieScrollbar(DemonObject):

    @staticmethod
    def declareORM(Type):
        DemonObject.declareORM(Type)
        Type.declareConst('ResourceMovieSlider')
        Type.declareConst('ResourceMovieBar')
        Type.declareConst('IsHorizontal')
        Type.declareParam('SetToZero')
        Type.declareParam('Value')

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
        self.initParam('SetToZero', params, True)
        self.initParam('Value', params, 0.0)