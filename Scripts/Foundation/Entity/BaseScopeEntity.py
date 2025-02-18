from Foundation.Entity.BaseEntity import BaseEntity
from Foundation.TaskManager import TaskManager

class BaseScopeEntity(BaseEntity):
    __metaclass__ = baseslots("tc")

    def __init__(self):
        super(BaseScopeEntity, self).__init__()

        self.tc = None
        pass

    def _onActivate(self):
        if self.tc is not None:
            self.tc.cancel()
            self.tc = None
            pass

        self.tc = TaskManager.createTaskChain()

        with self.tc as source:
            self._onScopeActivate(source)
            pass
        pass

    def _onScopeActivate(self, scope):
        pass

    def _onDeactivate(self):
        if self.tc is not None:
            self.tc.cancel()
            self.tc = None
            pass
        pass
    pass