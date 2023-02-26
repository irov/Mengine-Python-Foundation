import Trace
from GOAP2.GameManager import GameManager
from GOAP2.GroupManager import GroupManager

class GuardBlockInput(object):
    def __init__(self, source, enable=True, name=None, GroupName="BlockInput", SocketName="Socket_Click"):
        self.source = source
        self.enable = enable
        self.name = name

        self.GroupName = GroupName
        self.SocketName = SocketName
        pass

    @staticmethod
    def enableBlockSocket(value, GroupName="BlockInput", SocketName="Socket_Click"):
        socket = GroupManager.getObject(GroupName, SocketName)
        socket.setInteractive(value)

    def __blockInput(self, value):
        socket = GroupManager.getObject(self.GroupName, self.SocketName)

        socket.setInteractive(value)
        GameManager.blockKeyboard(value)

    def __enter__(self):
        if GroupManager.hasObject(self.GroupName, self.SocketName) is False:
            Trace.log("Object", 0, "GuardBlockInput invalid get object %s:%s" % (self.GroupName, self.SocketName))
            return self.source

        return self.source.makeGuardSource(self.enable, self.__blockInput)

    def __exit__(self, type, value, traceback):
        if type is not None:
            return False

        return True