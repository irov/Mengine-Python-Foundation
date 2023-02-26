from Foundation.DatabaseManager import DatabaseManager

class PolicyManager(object):
    s_policy = {}
    s_initialize = False

    @staticmethod
    def onFinalize():
        PolicyManager.s_policy = {}
        pass

    @staticmethod
    def loadParams(module, param):
        records = DatabaseManager.getDatabaseRecords(module, param)

        for record in records:
            Action = record.get("Action")
            Policy = record.get("Policy")

            PolicyManager.s_policy[Action] = Policy
            pass

        PolicyManager.s_initialize = True

        return True
        pass

    @staticmethod
    def hasPolicy(actionName):
        if PolicyManager.s_initialize is False:
            Trace.log("Manager", 0, "PolicyManager not initialize")
            return False
            pass

        return actionName in PolicyManager.s_policy
        pass

    @staticmethod
    def getPolicy(actionName, defaultPolicy=None):
        if PolicyManager.s_initialize is False:
            Trace.log("Manager", 0, "PolicyManager not initialize")
            return None
            pass

        if actionName not in PolicyManager.s_policy:
            return defaultPolicy
            pass

        policy = PolicyManager.s_policy[actionName]

        return policy

    @staticmethod
    def setPolicy(actionName, policyName):
        if PolicyManager.s_initialize is False:
            Trace.log("Manager", 0, "PolicyManager not initialize")
            return False

        PolicyManager.s_policy[actionName] = policyName
        return True

    @staticmethod
    def delPolicy(actionName):
        if PolicyManager.s_initialize is False:
            Trace.log("Manager", 0, "PolicyManager not initialize")
            return False

        if actionName in PolicyManager.s_policy:
            PolicyManager.s_policy.pop(actionName)
            return True
        return False