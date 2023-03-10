from MessageSender import MessageSender

class DefaultNode(MessageSender):
    def __init__(self):
        super(DefaultNode, self).__init__()

        self._callback = {}
        pass

    def addCallback(self, key, fn):
        if fn in self._callback[key]:
            print("Error! this callback is already in list", self, key, fn)
            return

        self._callback[key].append(fn)
        pass

    def removeCallback(self, key, fn):
        self._callback[key].remove(fn)
        pass