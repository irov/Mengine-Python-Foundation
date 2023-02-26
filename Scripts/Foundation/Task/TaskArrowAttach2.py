from Foundation.ArrowManager import ArrowManager
from Foundation.Task.MixinObject import MixinObject
from Foundation.Task.Task import Task

class TaskArrowAttach2(MixinObject, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskArrowAttach2, self)._onParams(params)
        self.Offset = params.get("Offset", False)
        self.Origin = params.get("Origin", False)
        pass

    def _onRun(self):
        ItemEntity = self.Object.getEntity()

        position = (0, 0)

        if self.Offset is True:
            ArrowPosition = Menge.getCursorPosition()
            ItemPosition = ItemEntity.getWorldPosition()
            position = (ArrowPosition.x - ItemPosition[0], ArrowPosition.y - ItemPosition[1])
            pass

        if ArrowManager.emptyArrowAttach() is False:
            attach = ArrowManager.getArrowAttach()
            attach.setParam("Enable", False)
            attachEntity = attach.getEntity()
            attachEntity.disable()
            pass

        ArrowManager.attachArrow(self.Object)
        arrow = ArrowManager.getArrow()

        if self.Origin is True:
            Image = ItemEntity.getSprite()
            origin = Image.getLocalImageCenter()

            itemPos = self.Object.getPosition()
            self.Object.setOrigin(origin)

            arrowPos = arrow.getLocalPosition()

            position = (itemPos[0] - arrowPos.x, itemPos[1] - arrowPos.y)
            pass

        self.Object.setParam("Enable", True)
        self.Object.setPosition(position)

        arrow.addChildFront(ItemEntity)
        return True
        pass
    pass