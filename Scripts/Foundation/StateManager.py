from Notification import Notification

class StateManager(object):
    s_states = {}

    @staticmethod
    def onFinalize():
        StateManager.s_states = {}
        pass

    @staticmethod
    def addState(id, value):
        if id in StateManager.s_states:
            return
            pass

        StateManager.s_states[id] = value
        pass

    @staticmethod
    def changeState(id, value, *args):
        if id not in StateManager.s_states:
            return
            pass

        StateManager.s_states[id] = value
        Notification.notify(Notificator.onStateChange, id, value, *args)
        pass

    @staticmethod
    def getState(id):
        if StateManager.hasState(id) is False:
            return None
            pass
        return StateManager.s_states[id]
        pass

    @staticmethod
    def hasState(id):
        return id in StateManager.s_states
        pass

    pass