class GuardBlockMusicVolumeFade(object):
    def __init__(self, source, Tag, To):
        self.source = source
        self.Tag = Tag
        self.To = To
        pass

    def __enter__(self):
        def __guard(value, tag, to):
            if value is True:
                Mengine.musicSetVolumeTag(tag, to, 1.0)
                pass
            else:
                Mengine.musicSetVolumeTag(tag, 1.0, to)
                pass
            pass

        return self.source.makeGuardSource(True, __guard, self.Tag, self.To)
        pass

    def __exit__(self, type, value, traceback):
        if type is not None:
            return False
            pass

        return True
        pass
    pass