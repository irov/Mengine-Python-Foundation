from Foundation.DatabaseManager import DatabaseManager


class PolicyManager(object):
    s_policy = {}

    @staticmethod
    def onFinalize():
        PolicyManager.s_policy = {}

    @staticmethod
    def loadParams(module, param):
        records = DatabaseManager.getDatabaseRecords(module, param)

        for record in records:
            Action = record.get("Action")
            Policy = record.get("Policy")

            PolicyManager.s_policy[Action] = Policy

        return True

    @staticmethod
    def hasPolicy(actionName):
        return actionName in PolicyManager.s_policy

    @staticmethod
    def getPolicy(actionName, defaultPolicy=None):
        if actionName not in PolicyManager.s_policy:
            return defaultPolicy

        policy = PolicyManager.s_policy[actionName]
        return policy

    @staticmethod
    def setPolicy(actionName, policyName):
        PolicyManager.s_policy[actionName] = policyName
        return True

    @staticmethod
    def delPolicy(actionName):
        if actionName in PolicyManager.s_policy:
            PolicyManager.s_policy.pop(actionName)
            return True
        return False
