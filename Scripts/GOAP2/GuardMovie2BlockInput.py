from GOAP2.GroupManager import GroupManager

class GuardMovie2BlockInput(object):
    def __init__(self, source, enable=True, name=None, GroupName="BlockInput", Movie2Name="Movie2_BlockInput"):
        self.source = source
        self.enable = enable
        self.name = name

        self.GroupName = GroupName
        self.Movie2Name = Movie2Name
        pass

    def __blockInput(self, value):
        movie = GroupManager.getObject(self.GroupName, self.Movie2Name)

        movie.setEnable(value)
        pass

    def __enter__(self):
        if GroupManager.hasObject(self.GroupName, self.Movie2Name) is False:
            Trace.log("Object", 0, "GuardMovie2BlockInput invalid get object %s:%s" % (self.GroupName, self.Movie2Name))
            return self.source
            pass

        return self.source.makeGuardSource(self.enable, self.__blockInput)
        pass

    def __exit__(self, type, value, traceback):
        if type is not None:
            return False
            pass

        return True
        pass
    pass