from Foundation.Manager import Manager

class StateManager(Manager):
    s_states = {}

    @staticmethod
    def _onFinalize():
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

        StateManager.s_states[id] = value
        Notification.notify(Notificator.onStateChange, id, value, *args)
        pass

    @staticmethod
    def getState(id):
        if StateManager.hasState(id) is False:
            return None
            pass
        return StateManager.s_states[id]

    @staticmethod
    def hasState(id):
        return id in StateManager.s_states