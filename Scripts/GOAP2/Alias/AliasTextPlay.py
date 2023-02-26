from GOAP2.Task.TaskAlias import TaskAlias

class AliasTextPlay(TaskAlias):
    def _onParams(self, params):
        super(AliasTextPlay, self)._onParams(params)

        self.ObjectText = params.get("ObjectText")
        self.TextID = params.get("TextID")
        self.TextDelay = params.get("TextDelay")
        self.AudioDuration = params.get("AudioDuration")
        pass

    def _onInitialize(self):
        super(AliasTextPlay, self)._onInitialize()

        if self.ObjectText is None:
            self.initializeFailed("ObjectText is None")
            pass

        if self.TextID is None:
            self.initializeFailed("TextID is None")
            pass
        pass

    def _onGenerate(self, source):
        source.addTask("TaskEnable", Object=self.ObjectText, Value=True)
        source.addTask("TaskTextSetTextID", Text=self.ObjectText, Value=self.TextID)

        if self.TextDelay != 0:
            source.addTask("AliasTextPlay2", ObjectText=self.ObjectText, TextID=self.TextID, TextDelay=self.TextDelay, AudioDuration=self.AudioDuration)
        pass
    pass