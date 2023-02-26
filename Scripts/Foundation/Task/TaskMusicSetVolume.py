from Foundation.Task.Task import Task

class TaskMusicSetVolume(Task):
    __metaclass__ = finalslots("Tag", "To", "From")

    Skiped = True

    def _onParams(self, params):
        super(TaskMusicSetVolume, self)._onParams(params)

        self.Tag = params.get("Tag", "Generic")
        self.To = params.get("To")
        self.From = params.get("From")
        pass

    def _onRun(self):
        Menge.musicSetVolumeTag(self.Tag, self.To, self.From)

        return True
        pass
    pass