from Foundation.System import System
from Foundation.DefaultManager import DefaultManager
from Foundation.SceneManager import SceneManager


class SystemContentEdges(System):

    def _onRun(self):
        with self.createTaskChain(Name="ContentEdgesCreator") as tc:
            tc.addListener(Notificator.onRun)
            tc.addFunction(self.enableContentEdgesBackground)
        return True

    def enableContentEdgesBackground(self):
        content_edge_background_name = self.getAspectRatioContentEdgeModeSlotName()

        if content_edge_background_name is None:
            return

        def _visitor(scene_description):
            if content_edge_background_name not in scene_description.slots:
                return

            slot = scene_description.slots[content_edge_background_name]
            slot["Enable"] = True

        SceneManager.visitSceneDescriptions(_visitor)

    @staticmethod
    def getAspectRatioContentEdgeModeSlotName():
        aspect_ratio_mode = Mengine.getAspectRatioContentEdgeMode()

        Trace.msg_dev("!!!!!!!!!!!!!!!!! aspect_ratio_mode: {!r}".format(aspect_ratio_mode))

        if aspect_ratio_mode == Mengine.ECEM_NONE:
            return None
        elif aspect_ratio_mode == Mengine.ECEM_HORIZONTAL_CONTENT_EDGE:
            return DefaultManager.getDefault("HorizontalContentEdgesSlotName", "BackgroundHorizontal")
        elif aspect_ratio_mode == Mengine.ECEM_VERTICAL_CONTENT_EDGE:
            return DefaultManager.getDefault("VerticalContentEdgesSlotName", "BackgroundVertical")

