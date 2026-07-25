from Foundation.BaseEntity import BaseEntity
from Foundation.ObjectManager import ObjectManager
from Foundation.TaskManager import TaskManager
from Foundation.VirtualAreaHelper import createVirtualArea, setupVirtualAreaWithMovie, destroyVirtualArea

class MovieVirtualArea(BaseEntity):
    @staticmethod
    def declareORM(Type):
        BaseEntity.declareORM(Type)
        Type.addAction('ResourceMovieFrame')
        Type.addAction('ResourceMovieContent')

        Type.addAction('Rigidity')
        Type.addAction('Friction')

        Type.addAction('DraggingMode')
        Type.addAction('EnableScale')
        Type.addAction('MaxScaleFactor')

    def __init__(self):
        super(MovieVirtualArea, self).__init__()

        self._content_resource = None
        self._frame = None
        self._content = None

        self._virtual_area = None

    def _onInitialize(self, obj):
        super(MovieVirtualArea, self)._onInitialize(obj)

        def create_movie(name, resource_name, enable):
            if Mengine.hasResource(resource_name) is False:
                # Trace.log()
                Trace.log("Entity", 0, '************************** no movies')
                return

            resource = Mengine.getResourceReference(resource_name)

            movie = ObjectManager.createObjectUnique('Movie', name, self.object, ResourceMovie=resource)
            self.addChild(movie.getEntityNode())

            movie.setEnable(enable)

            return movie

        self._content = create_movie('Content', self.ResourceMovieContent, True)
        self._frame = create_movie('Frame', self.ResourceMovieFrame, True)

        self._content_resource = Mengine.getResourceReference(self.ResourceMovieContent)
        return True

    def _onActivate(self):
        self._virtual_area = createVirtualArea(
            friction=self.Friction,
            rigidity=self.Rigidity,
            dragging_mode=self.DraggingMode,
            enable_scale=self.EnableScale,
            max_scale=self.MaxScaleFactor
        )

        if self._content_resource.hasBoundBox():
            box = self._content_resource.getBoundBox()
            self._virtual_area.setVirtualAreaContentSize(0, 0, box.maximum.x - box.minimum.x, box.maximum.y - box.minimum.y)

        anchor = self._content.getMovieNode('anchor_solid').getWorldPosition().y

        self._virtual_area.addVirtualAreaContentNode(self._content.getEntityNode(), False)
        self._virtual_area.addVirtualAreaContentNode(self._content.getMovieNode('anchor_solid'), True)
        setupVirtualAreaWithMovie(self._virtual_area, self._frame, 'socket')

        self._virtual_area.setVirtualAreaSnappingMode(Mengine.EVASM_VERTICAL)
        self._virtual_area.setVirtualAreaSnappingBoundsPoint(Mengine.vec2f(0.0, 0.0))

        for child in self._content.getMovie().getAllChildren():
            self._virtual_area.addVirtualAreaSnappingPoint(child.getWorldPosition().y - anchor)

        with TaskManager.createTaskChain(Repeat=True) as tc:
            tc.addTask('TaskKeyPress', Keys=(Mengine.KC_P,))

            def _print():
                with Utils.DebugPrinter('Iteration'):
                    pass
            tc.addFunction(_print)

    def _onDeactivate(self):
        super(MovieVirtualArea, self)._onDeactivate()

        if self._virtual_area is not None:
            destroyVirtualArea(self._virtual_area)
            self._virtual_area = None
