from Foundation.Providers.LeaderboardProvider import LeaderboardProvider


class DummyLeaderboard(object):
    @staticmethod
    def setProvider():
        LeaderboardProvider.setProvider("Dummy", dict(
            submitLeaderboardScore=DummyLeaderboard.submitLeaderboardScore,
            showLeaderboard=DummyLeaderboard.showLeaderboard,
        ))

    @staticmethod
    def submitLeaderboardScore(leaderboard_id, score):
        Trace.msg("DUMMY submitLeaderboardScore {} {}".format(leaderboard_id, score))
        return True

    @staticmethod
    def showLeaderboard(leaderboard_id):
        Trace.msg("DUMMY showLeaderboard {}".format(leaderboard_id))
        return True
