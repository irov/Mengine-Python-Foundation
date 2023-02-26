from GOAP2.Task.MixinObserver import MixinObserver
from GOAP2.Task.Task import Task
from GOAP3.ZoomManager import ZoomManager

class TaskZoomInterrupt(MixinObserver, Task):
    Skiped = True

    def _onRun(self):
        OpenZoom = ZoomManager.getZoomOpen()
        if OpenZoom is None:
            return True

        ZoomOpenGroupName = ZoomManager.getZoomOpenGroupName()

        ZoomManager.closeZoom(ZoomOpenGroupName)

        if OpenZoom.hasObject() is False:
            return True
            pass

        ZoomObject = OpenZoom.getObject()

        Enable = ZoomObject.getParam("Enable")

        if Enable is True:
            ZoomObject.setParam("Enable", False)
            pass

        return True
        pass
    pass