from GOAP2.Systems.SystemGoogleServices import SystemGoogleServices
from GOAP2.Task.TaskAlias import TaskAlias

class PolicyExternalAchieveProgressGooglePlay(TaskAlias):

    def _onParams(self, params):
        self.AchieveId = params["AchieveId"]
        self.Complete = params.get("Complete", False)
        self.IncreaseSteps = params.get("IncreaseSteps", 0)

    def _onInitialize(self):
        if self.IncreaseSteps < 0:
            self.initializeFailed("IncreaseSteps must be positive")

    def action(self):
        if self.IncreaseSteps > 0:
            SystemGoogleServices.incrementAchievement(self.AchieveId, self.IncreaseSteps)
        if self.Complete is True:
            SystemGoogleServices.unlockAchievement(self.AchieveId)

    def _onGenerate(self, source):
        source.addFunction(self.action)