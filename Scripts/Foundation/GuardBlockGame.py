from Foundation.GameManager import GameManager

class GuardBlockGame(object):
    def __init__(self, source):
        self.source = source
        pass

    def __blockGame(self, value):
        GameManager.blockGame(value)
        pass

    def __enter__(self):
        self.source.addTask("TaskGameUnblock")

        return self.source.makeGuardSource(True, self.__blockGame)
        pass

    def __exit__(self, type, value, traceback):
        if type is not None:
            return False
            pass

        return True
        pass
    pass