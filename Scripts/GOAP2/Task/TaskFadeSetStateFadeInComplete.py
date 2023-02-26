from GOAP2.Task.MixinGroup import MixinGroup
from GOAP2.Task.Task import Task

class TaskFadeSetStateFadeInComplete(MixinGroup, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskFadeSetStateFadeInComplete, self)._onParams(params)

        demonNameSuffix = params.get("DemonNameSuffix", None)
        self.demonName = "Demon_Fade"
        if demonNameSuffix:
            self.demonName = "%s_%s" % (self.demonName, demonNameSuffix)
            pass

        self.Demon_Fade = None
        pass

    def _onInitialize(self):
        super(TaskFadeSetStateFadeInComplete, self)._onInitialize()

        if _DEVELOPMENT is True:
            if self.Group.hasObject(self.demonName) is False:
                self.initializeFailed("Group %s not found %s" % (self.Group.getName(), self.demonName))
                pass
            pass

        self.Demon_Fade = self.Group.getObject(self.demonName)
        pass

    def _onCheck(self):
        if self.Demon_Fade.isActive() is False:
            return False
            pass

        Demon_FadeEntity = self.Demon_Fade.getEntity()

        if Demon_FadeEntity.isActivate() is False:
            return False
            pass

        return True
        pass

    def _onRun(self):
        Demon_FadeEntity = self.Demon_Fade.getEntity()
        Demon_FadeEntity.state = Demon_FadeEntity.FADE_IN_COMPLETE

        return True
        pass

    pass