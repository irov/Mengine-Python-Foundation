from Task import Task

class TaskObjectTextSetMaxVisibleChar(Task):
    Skiped = True

    def _onParams(self, params):
        super(TaskObjectTextSetMaxVisibleChar, self)._onParams(params)

        self.Text = params.get("Text")
        self.Iterator = params.get("Iterator")
        pass

    def _onRun(self):
        Value = 0
        if self.Iterator is None:
            TextEntity = self.Text.getEntity()
            TextField = TextEntity.getTextField()

            Value = TextField.getCharCount()
            pass
        else:
            Value = self.Iterator.getValue()
            pass

        self.Text.setMaxVisibleChar(Value)

        return True
        pass
    pass