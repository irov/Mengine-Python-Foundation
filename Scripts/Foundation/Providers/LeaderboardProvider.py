from Foundation.Providers.BaseProvider import BaseProvider


class LeaderboardProvider(BaseProvider):
    s_allowed_methods = [
        "submitLeaderboardScore",
        "showLeaderboard",
    ]

    @staticmethod
    def _setDevProvider():
        from Foundation.Providers.DummyLeaderboard import DummyLeaderboard
        DummyLeaderboard.setProvider()

    @staticmethod
    def submitLeaderboardScore(leaderboard_id, score):
        return LeaderboardProvider._call("submitLeaderboardScore", leaderboard_id, score)

    @staticmethod
    def showLeaderboard(leaderboard_id):
        return LeaderboardProvider._call("showLeaderboard", leaderboard_id)
