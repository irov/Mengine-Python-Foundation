from GOAP2.Object.DemonObject import DemonObject

class ObjectMovieVirtualArea(DemonObject):

    @staticmethod
    def declareORM(Type):
        DemonObject.declareORM(Type)
        Type.addConst(Type, 'ResourceMovieFrame')
        Type.addConst(Type, 'ResourceMovieContent')

        Type.addConst(Type, 'Rigidity')  # Elasticity friction
        Type.addConst(Type, 'Friction')  # Inertia friction

        Type.addConst(Type, 'DraggingMode')
        Type.addConst(Type, 'EnableScale')
        Type.addConst(Type, 'MaxScaleFactor')

    def _onParams(self, params):
        super(ObjectMovieVirtualArea, self)._onParams(params)
        self.initConst('ResourceMovieFrame', params, None)
        self.initConst('ResourceMovieContent', params, None)

        self.initConst('Rigidity', params, 0.5)
        self.initConst('Friction', params, 0.5)
        self.initConst('DraggingMode', params, 'free')
        self.initConst('EnableScale', params, True)
        self.initConst('MaxScaleFactor', params, 6.0)