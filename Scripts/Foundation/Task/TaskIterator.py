from Foundation.Task.Task import Task

class TaskIterator(Task):
    __metaclass__ = finalslots("Iterator", "Incref")

    Skiped = True

    def _onParams(self, params):
        super(TaskIterator, self)._onParams(params)

        self.Iterator = params.get("Iterator")
        self.Incref = params.get("Incref", 1)
        pass

    def _onValidate(self):
        super(TaskIterator, self)._onValidate()

        if isinstance(self.Iterator, Iterator) is False:
            self.validateFailed("Iterator '%s' is not Iterator type" % (self.Iterator))
            pass
        pass

    def _onRun(self):
        self.Iterator.incref(self.Incref)

        return True
        pass
    pass