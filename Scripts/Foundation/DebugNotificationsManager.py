from Foundation.DatabaseManager import DatabaseManager
from Foundation.Manager import Manager

class DebugNotificationsManager(Manager):
    s_data = []

    class LoggerParam(object):
        def __init__(self, identity, message, show_args):
            self.identity = identity
            self.message = message
            self.show_args = show_args

        def get(self, attr):
            return self.__dict__.get(attr)

        def __repr__(self):
            return "<LoggerParam [{}] {}>".format(self.identity, self.__dict__)

    @staticmethod
    def loadParams(module, name):
        records = DatabaseManager.getDatabaseRecords(module, name)

        for record in records:
            identity = record.get("Identity")
            message = record.get("Message")
            show_args = bool(record.get("PrintArgs", True))

            if identity is None:
                Trace.log("Manager", 0, "DebugNotificationsManager: you must add identity for row with message {!r}".format(message))
                continue
            elif Notificator.hasIdentity(identity) is False:
                Trace.log("Manager", 0, "DebugNotificationsManager: unregistered notificator identity {!r}".format(identity))
                continue

            params = DebugNotificationsManager.LoggerParam(identity, message, show_args)
            DebugNotificationsManager.s_data.append(params)

        return True

    @staticmethod
    def getAllData():
        return DebugNotificationsManager.s_data