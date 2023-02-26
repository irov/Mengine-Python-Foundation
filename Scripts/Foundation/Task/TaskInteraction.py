from Foundation.ArrowManager import ArrowManager
from Foundation.Task.MixinObjectTemplate import MixinInteraction
from Foundation.Task.MixinObserver import MixinObserver
from Foundation.Task.Task import Task

class TaskInteraction(MixinInteraction, MixinObserver, Task):
    def _onParams(self, params):
        super(TaskInteraction, self)._onParams(params)

        self.AutoEnable = params.get("AutoEnable", True)
        pass

    def _onRun(self):
        if self.AutoEnable is True:
            self.Interaction.setInteractive(True)
            pass

        self.addObserverFilter(Notificator.onInteractionClick, self.__onInteractionClick, self.Interaction)

        return False
        pass

    def _onFinally(self):
        super(TaskInteraction, self)._onFinally()

        if self.AutoEnable is True:
            self.Interaction.setInteractive(False)
            pass
        pass

    def __onInteractionClick(self, interaction):
        if ArrowManager.emptyArrowAttach() is False:
            return False
            pass

        return True
        pass
    pass