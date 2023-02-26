from Foundation.Systems.SystemAppleServices import SystemAppleServices
from Foundation.Task.TaskAlias import TaskAlias

class PolicyExternalAchieveProgressAppleGameCenter(TaskAlias):

    def _onParams(self, params):
        self.AchieveId = params["AchieveId"]
        self.Complete = params.get("Complete", False)
        self.Percents = params.get("Percents", 0)

        if self.Percents > 1 or self.Complete is True:
            self.Percents = 1

        self.Percents *= 100.0

    def _onInitialize(self):
        if self.Percents < 0:
            self.initializeFailed("Percents must be positive float from 0 to 1")

    def action(self):
        SystemAppleServices.sendAchievementToGameCenter(self.AchieveId, self.Percents)

    def _onGenerate(self, source):
        source.addFunction(self.action)