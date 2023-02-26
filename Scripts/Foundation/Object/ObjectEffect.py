# from ObjectAnimatable import ObjectAnimatable
#
# class ObjectEffect(ObjectAnimatable):
#     @staticmethod
#     def declareORM(Type):
#         ObjectAnimatable.declareORM(Type)
#
#         Type.addResource(Type, "ResourceName")
#         Type.addParam(Type, "EmitterRelative")
#         Type.addParam(Type, "Polygon")
#         Type.addParam(Type, "EmitterImage")
#         Type.addParam(Type, "EmitterPolygon")
#         Type.addParam(Type, "TranslateWithParticle")
#         Type.addParam(Type, "EmitterRandomMode")
#         Type.addParam(Type, "EmitterName")
#         pass
#
#     def _onParams(self, params):
#         super(ObjectEffect, self)._onParams(params)
#
#         self.initResource("ResourceName", params, None)
#
#         self.initParam("EmitterRelative", params, False)
#         self.initParam("Polygon", params, None)
#         self.initParam("EmitterImage", params, None)
#         self.initParam("EmitterPolygon", params, None)
#         self.initParam("TranslateWithParticle", params, True)
#         self.initParam("EmitterRandomMode", params, False)
#
#         Name = self.getName()
#         self.initParam("EmitterName", params, Name)
#         pass
#     pass