from Foundation.Identity import Identity

class NotificatorCollection(object):
    def addIdentities(self, notifiers):
        for notify in notifiers:
            self.addIdentity(notify)
            pass
        pass

    def hasIdentity(self, notify):
        if notify not in self.__dict__:
            return False
            pass

        return True
        pass

    def addIdentity(self, notify):
        if _DEVELOPMENT is True:
            if notify in self.__dict__:
                Trace.log("Notification", 0, "Notificator.addIdentity already exist '%s'" % (notify))
                pass
            pass

        self.__dict__[notify] = Identity(notify)
        pass

    def getIdentity(self, stringIdentity):
        if stringIdentity is None:
            Trace.log("Notification", 0, "Notificator.getIdenntity can't apply <None> as arg. ")
            return None
            pass

        identity = self.__dict__.get(stringIdentity)

        if identity is None:
            Trace.log("Notification", 0, "Notificator.getIdenntity unregister %s" % (stringIdentity,))
            pass

        return identity
        pass
    pass

Notificator = NotificatorCollection()  # coz need 1 at least one member of the class