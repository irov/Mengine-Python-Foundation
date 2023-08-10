from Foundation.Providers.BaseProvider import BaseProvider


class AchievementsProvider(BaseProvider):
    s_allowed_methods = [
        "incrementAchievement",
        "setAchievementProgress",
        "unlockAchievement",
        "showAchievements",
    ]

    @staticmethod
    def incrementAchievement(achievement_id, steps):
        if steps is not None and steps < 1:
            Trace.log("Provider", 0, "ValueError: steps cannot be a positive value (not {})".format(steps))
            return

        return AchievementsProvider._call("incrementAchievement", achievement_id, steps)

    @staticmethod
    def setAchievementProgress(achievement_id, current_step, total_steps):
        """ do things inside provider (increment or unlock) """
        return AchievementsProvider._call("setAchievementProgress", achievement_id, current_step, total_steps)

    @staticmethod
    def unlockAchievement(achievement_id):
        return AchievementsProvider._call("unlockAchievement", achievement_id)

    @staticmethod
    def showAchievements():
        return AchievementsProvider._call("showAchievements")


class DummyAchievements(object):

    @staticmethod
    def setProvider():
        AchievementsProvider.setProvider("Dummy", dict(
            incrementAchievement=DummyAchievements.incrementAchievement,
            unlockAchievement=DummyAchievements.unlockAchievement,
            setAchievementProgress=DummyAchievements.setAchievementProgress,
            showAchievements=DummyAchievements.showAchievements,
        ))

    @staticmethod
    def incrementAchievement(achievement_id, steps):
        Trace.msg("DUMMY incrementAchievement {} {}".format(achievement_id, steps))

    @staticmethod
    def setAchievementProgress(achievement_id, current_step, total_steps):
        """ do things inside provider (increment or unlock) """
        percent = round((float(current_step) / float(total_steps)) * 100.0, 1)
        Trace.msg("DUMMY setAchievementProgress {} {}%% ({}/{})".format(achievement_id, percent, current_step, total_steps))


    @staticmethod
    def unlockAchievement(achievement_id):
        Trace.msg("DUMMY unlockAchievement {}".format(achievement_id))

    @staticmethod
    def showAchievements():
        Trace.msg("DUMMY showAchievements...")




