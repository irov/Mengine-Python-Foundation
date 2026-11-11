from Foundation.GameManager import GameManager

class GuardBlockGame(object):
    def __init__(self, source):
        self.source = source
        pass

    def __enter__(self):
        def __blockGame(value):
            GameManager.blockGame(value)
            pass

        self.source.addTask("TaskGameUnblock")

        return self.source.makeGuardSource(True, __blockGame)
        pass

    def __exit__(self, type, value, traceback):
        if type is not None:
            return False
            pass

        return True
        pass
    pass