from GOAP2.Task.Task import Task

class TaskMountPak(Task):
    def _onParams(self, params):
        super(TaskMountPak, self)._onParams(params)

        self.Group = params.get("Group", "")
        self.Description = params.get("Description")
        self.FileType = params.get("FileType")
        self.FileName = params.get("FileName")
        self.Category = params.get("Category")
        self.Path = params.get("Path", '{}/{}.{}'.format(self.Group, self.FileName, self.FileType))
        pass

    def _onRun(self):
        Menge.mountResourcePak(self.Group, self.FileName, self.FileType, self.Category, self.Path, self.Description)
        return True
        pass
    pass