class MessageSender(object):
    def __init__(self):
        super(MessageSender, self).__init__()
        self._messages = {}
        pass

    def addReciever(self, message, reciever):
        if message not in self._messages:
            self._messages[message] = []

        if reciever not in self._messages[message]:
            self._messages[message].append(reciever)
            return True
        return False

    def removeReciever(self, message, reciever):
        if message not in self._messages:
            return False

        if reciever in self._messages[message]:
            self._messages[message].remove(reciever)
            return True
        return False

    def sendMessage(self, message, *args):
        if message not in self._messages:
            return

        for reciever in self._messages[message]:
            reciever(*args)
            pass
        pass

    def addRecievers(self, **recievers):
        for message, reciever in recievers.iteritems():
            self.addReciever(message, reciever)
        pass

    def removeRecievers(self, **recievers):
        for message, reciever in recievers.iteritems():
            self.removeReciever(message, reciever)
        pass
    pass