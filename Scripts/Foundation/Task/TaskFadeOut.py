from Foundation.DefaultManager import DefaultManager
from Foundation.SystemManager import SystemManager
from Foundation.Task.MixinGroup import MixinGroup
from Foundation.Task.Task import Task

class TaskFadeOut(MixinGroup, Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskFadeOut, self)._onParams(params)

        self.From = params.get("From", 1)

        DefaultFadeOutTime = DefaultManager.getDefaultFloat("DefaultFadeOutTime", 1000.0)
        self.Time = params.get("Time", DefaultFadeOutTime)

        self.FromIdle = params.get("FromIdle", False)
        self.reset_fade_count = params.get("ResetFadeCount", False)

        demonNameSuffix = params.get("DemonNameSuffix", None)
        self.easing = params.get("Easing", "easyLinear")
        self.demonName = "Demon_Fade"
        if demonNameSuffix:
            self.demonName = "%s_%s" % (self.demonName, demonNameSuffix)
            pass

        self.Demon_Fade = None
        self.system_fade = SystemManager.getSystem("SystemFade")

    def _onInitialize(self):
        super(TaskFadeOut, self)._onInitialize()

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

        if self.FromIdle is False and Demon_FadeEntity.state == Demon_FadeEntity.FADE_IDLE:
            return False
            pass

        if self.reset_fade_count is True:
            self.system_fade.clearFadeCount()
            return True

        self.system_fade.decFadeCount()
        current_fade_count = self.system_fade.getFadeCount()

        # print '[FADE DBG] TaskFadeOut Demon "{}" decrement fade_count: {}'.format(
        #     Demon_FadeEntity.getName(), current_fade_count)

        if self.system_fade.getFadeCount() < 0:  # !!! appear next bug: https://trello.com/c/zif6ggEW/613-%D1%84%D0%B5%D0%B9%D0%B4-%D0%B1%D0%B0%D0%B3
            # print '[FADE DBG] [CHECK FALSE] TaskFadeOut Demon "{}" CHECK 4 -> fade_count < 0'.format(
            #     Demon_FadeEntity.getName())
            return False

        self.system_fade.decFadeCount()

        return True
        pass

    def _onRun(self):
        Demon_FadeEntity = self.Demon_Fade.getEntity()
        Demon_FadeEntity.fadeOut(self.From, self.Time, self._onFadeOutComplete, self.easing)
        # print '[FADE DBG] TaskFadeOut Demon "{}" FADE-OUT'.format(self.Demon_Fade.getName())
        return False
        pass

    def _onSkip(self):
        Demon_FadeEntity = self.Demon_Fade.getEntity()
        Demon_FadeEntity.stopFade()
        pass

    def _onFadeOutComplete(self, isEnd):
        self.complete()
        pass
    pass