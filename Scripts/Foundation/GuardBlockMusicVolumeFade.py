class GuardBlockMusicVolumeFade(object):
    def __init__(self, source, Tag, To):
        self.source = source
        self.Tag = Tag
        self.To = To
        pass

    def __guard(self, value):
        if value is True:
            Mengine.musicSetVolumeTag(self.Tag, self.To, 1.0)
            pass
        else:
            Mengine.musicSetVolumeTag(self.Tag, 1.0, self.To)
            pass
        pass

    def __enter__(self):
        return self.source.makeGuardSource(True, self.__guard)
        pass

    def __exit__(self, type, value, traceback):
        if type is not None:
            return False
            pass

        return True
        pass
    pass