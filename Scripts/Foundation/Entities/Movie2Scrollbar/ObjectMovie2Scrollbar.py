from Foundation.Object.DemonObject import DemonObject

class ObjectMovie2Scrollbar(DemonObject):

    @staticmethod
    def declareORM(Type):
        DemonObject.declareORM(Type)

        Type.addConst(Type, 'ResourceMovie')

        Type.addConst(Type, 'CompositionNameSlider')
        Type.addConst(Type, 'CompositionNameBar')

        Type.addConst(Type, 'IsHorizontal')
        Type.addParam(Type, 'Value')

    def __init__(self):
        super(ObjectMovie2Scrollbar, self).__init__()

        self.onScroll = Event('onScroll')
        self.onScrollEnd = Event('onScrollEnd')
        self.onScrollStart = Event('onScrollStart')

    def _onParams(self, params):
        super(ObjectMovie2Scrollbar, self)._onParams(params)
        self.initConst('ResourceMovie', params, None)

        self.initConst('CompositionNameSlider', params, None)
        self.initConst('CompositionNameBar', params, None)

        self.initConst('IsHorizontal', params, False)
        self.initParam('Value', params, 0.0)