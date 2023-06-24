from Foundation.DefaultManager import DefaultManager
from Foundation.Task.TaskAlias import TaskAlias

class AliasTextPlay2(TaskAlias):
    def _onParams(self, params):
        super(AliasTextPlay2, self)._onParams(params)

        self.ObjectText = params.get("ObjectText")
        self.TextID = params.get("TextID")
        self.TextDelay = params.get("TextDelay")
        self.AudioDuration = params.get("AudioDuration")
        pass

    def _onGenerate(self, source):
        if self.TextDelay is None:
            self.TextDelay = DefaultManager.getDefaultFloat("DialogTextLetterDelay", 0.05)
            pass

        if self.AudioDuration is not None:
            text = Mengine.getTextFromId(self.TextID)
            text_length = len(text)
            self.TextDelay = float(self.AudioDuration) / float(text_length)

        self.TextDelay *= 1000.0

        TextEntity = self.ObjectText.getEntity()

        TextField = TextEntity.getTextField()
        TextCharCount = TextField.getCharCount()

        with source.addRaceTask(2) as (play, skip):
            with play.addForTask(TextCharCount + 1) as (it, source_char):
                source_char.addTask("TaskObjectTextSetMaxVisibleChar", Text=self.ObjectText, Iterator=it)
                source_char.addTask("TaskDelay", Time=self.TextDelay)

            skip.addDelay(300)
            skip.addTask("TaskMouseButtonClick", isDown=False)
            skip.addTask("TaskObjectTextSetMaxVisibleChar", Text=self.ObjectText)