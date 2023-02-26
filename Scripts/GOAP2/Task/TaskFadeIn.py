from GOAP2.DefaultManager import DefaultManager
from GOAP2.SystemManager import SystemManager
from GOAP2.Task.MixinGroup import MixinGroup
from GOAP2.Task.Task import Task

class TaskFadeIn(MixinGroup, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskFadeIn, self)._onParams(params)
        self.fadeTo = params.get("To", 1)

        DefaultFadeInTime = DefaultManager.getDefaultFloat("DefaultFadeInTime", 500.0)
        self.time = params.get("Time", DefaultFadeInTime)

        demonNameSuffix = params.get("DemonNameSuffix", None)
        self.demonName = "Demon_Fade"
        self.easing = params.get("Easing", "easyLinear")
        if demonNameSuffix:
            self.demonName = "%s_%s" % (self.demonName, demonNameSuffix)
            pass
        self.Demon_Fade = None
        self.system_fade = SystemManager.getSystem("SystemFade")

    def _onInitialize(self):
        super(TaskFadeIn, self)._onInitialize()

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

        self.system_fade.incFadeCount()
        current_fade_count = self.system_fade.getFadeCount()

        return True
        pass

    def _onRun(self):
        Demon_FadeEntity = self.Demon_Fade.getEntity()
        Demon_FadeEntity.fadeIn(self.fadeTo, self.time, self._onFadeInComplete, self.easing)
        return False
        pass

    def _onSkip(self):
        Demon_FadeEntity = self.Demon_Fade.getEntity()
        Demon_FadeEntity.stopFade()
        pass

    def _onFadeInComplete(self, isEnd):
        self.complete()
        pass
    pass