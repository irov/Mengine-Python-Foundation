from Foundation.Object.DemonObject import DemonObject

class ObjectMovieVirtualArea(DemonObject):

    @staticmethod
    def declareORM(Type):
        DemonObject.declareORM(Type)
        Type.declareConst('ResourceMovieFrame')
        Type.declareConst('ResourceMovieContent')

        Type.declareConst('Rigidity')  # Elasticity friction
        Type.declareConst('Friction')  # Inertia friction

        Type.declareConst('DraggingMode')
        Type.declareConst('EnableScale')
        Type.declareConst('MaxScaleFactor')

    def _onParams(self, params):
        super(ObjectMovieVirtualArea, self)._onParams(params)
        self.initConst('ResourceMovieFrame', params, None)
        self.initConst('ResourceMovieContent', params, None)

        self.initConst('Rigidity', params, 0.5)
        self.initConst('Friction', params, 0.5)
        self.initConst('DraggingMode', params, 'free')
        self.initConst('EnableScale', params, True)
        self.initConst('MaxScaleFactor', params, 6.0)