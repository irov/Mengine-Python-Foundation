from Foundation.BaseEntity import BaseEntity
from Foundation.TaskManager import TaskManager

class BaseScopeEntity(BaseEntity):
    __metaclass__ = baseslots("tc")

    ENTITY_SCOPE_REPEAT = False

    @staticmethod
    def declareORM(Type):
        BaseEntity.declareORM(Type)
        pass

    def __init__(self):
        super(BaseScopeEntity, self).__init__()

        self.tc = None
        pass

    def _onScopeUntil(self):
        return False

    def _onActivate(self):
        if self.tc is not None:
            self.tc.cancel()
            self.tc = None
            pass

        self.tc = TaskManager.createTaskChain(Repeat = self.ENTITY_SCOPE_REPEAT, Until=self._onScopeUntil, Group = self.object.Group)

        with self.tc as source:
            self._onScopeActivate(source)
            pass
        pass

    def _onScopeActivate(self, source):
        pass

    def _onDeactivate(self):
        self._onScopeDeactivate()

        if self.tc is not None:
            self.tc.cancel()
            self.tc = None
            pass
        pass

    def _onScopeDeactivate(self):
        pass
    pass