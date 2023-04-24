from Foundation.Providers.BaseProvider import BaseProvider


class AchievementsProvider(BaseProvider):
    s_allowed_methods = [
        "incrementAchievement",
        "unlockAchievement",
        "showAchievements",
    ]

    @staticmethod
    def incrementAchievement(achievement_id, steps):
        if steps is not None and steps < 1:
            Trace.log("Provider", 0, "ValueError: steps cannot be 0 or negative value (not {})".format(steps))
            return

        return AchievementsProvider._call("incrementAchievement", achievement_id, steps)

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
            showAchievements=DummyAchievements.showAchievements,
        ))

    @staticmethod
    def incrementAchievement(achievement_id, steps):
        Trace.msg("DUMMY incrementAchievement {} {}".format(achievement_id, steps))

    @staticmethod
    def unlockAchievement(achievement_id):
        Trace.msg("DUMMY unlockAchievement {}".format(achievement_id))

    @staticmethod
    def showAchievements():
        Trace.msg("DUMMY showAchievements...")




