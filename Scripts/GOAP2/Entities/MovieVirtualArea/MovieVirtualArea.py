from GOAP2 import TaskManager
from GOAP2.Entity.BaseEntity import BaseEntity
from GOAP2.ObjectManager import ObjectManager
from GOAP2.Vector2D import Vector2D

from VirtualArea import VirtualArea

class MovieVirtualArea(BaseEntity):
    @staticmethod
    def declareORM(Type):
        BaseEntity.declareORM(Type)
        Type.addAction(Type, 'ResourceMovieFrame')
        Type.addAction(Type, 'ResourceMovieContent')

        Type.addAction(Type, 'Rigidity')
        Type.addAction(Type, 'Friction')

        Type.addAction(Type, 'DraggingMode')
        Type.addAction(Type, 'EnableScale')
        Type.addAction(Type, 'MaxScaleFactor')

    def __init__(self):
        super(MovieVirtualArea, self).__init__()

        self._content_resource = None
        self._frame = None
        self._content = None

        self._virtual_area = None

    def _onInitialize(self, obj):
        super(MovieVirtualArea, self)._onInitialize(obj)

        def create_movie(name, resource_name, enable):
            if Menge.hasResource(resource_name) is False:
                # Trace.log()
                Trace.log("Entity", 0, '************************** no movies')
                return

            resource = Menge.getResourceReference(resource_name)

            movie = ObjectManager.createObjectUnique('Movie', name, self.object, ResourceMovie=resource)
            self.addChild(movie.getEntityNode())

            movie.setEnable(enable)

            return movie

        self._content = create_movie('Content', self.ResourceMovieContent, True)
        self._frame = create_movie('Frame', self.ResourceMovieFrame, True)

        self._content_resource = Menge.getResourceReference(self.ResourceMovieContent)
        return True

    def _onActivate(self):
        self._virtual_area = VirtualArea()
        self.virtual_area.onInitialize(friction=self.Friction, rigidity=self.Rigidity, dragging_mode=self.DraggingMode, enable_scale=self.EnableScale, max_scale=self.MaxScaleFactor)

        if self._content_resource.hasBoundBox():
            box = self._content_resource.getBoundBox()
            self._virtual_area.set_content_size(0, 0, box.maximum.x - box.minimum.x, box.maximum.y - box.minimum.y)

        anchor = self._content.getMovieNode('anchor_solid').getWorldPosition().y

        self._virtual_area.add_node(self._content.getEntityNode())
        self._virtual_area.add_node(self._content.getMovieNode('anchor_solid'), use_as_anchor=True)
        self._virtual_area.setup_with_movie(self._frame, 'socket')

        snapping = self._virtual_area.get_snapping()

        snapping.set_to_Y_axis()
        snapping.set_bounds_point(Vector2D())

        for child in self._content.getMovie().getAllChildren():
            snapping.add_snapper(child.getWorldPosition().y - anchor)

        with TaskManager.createTaskChain(Repeat=True) as tc:
            tc.addTask('TaskKeyPress', Keys=(Menge.KC_P,))

            def _print():
                with Utils.DebugPrinter('Iteration'):
                    pass
            tc.addFunction(_print)

    def _onDeactivate(self):
        super(MovieVirtualArea, self)._onDeactivate()

        # del self._virtual_area
        if self._virtual_area is not None:
            self._virtual_area.onFinalize()
            self._virtual_area = None