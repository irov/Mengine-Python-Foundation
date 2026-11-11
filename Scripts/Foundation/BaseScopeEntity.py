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

    def _getScopeGroup(self):
        return self.object.Group

    def _onActivate(self):
        super(BaseScopeEntity, self)._onActivate()

        self.__cancelScope()

        self.tc = TaskManager.createTaskChain(Repeat=self.ENTITY_SCOPE_REPEAT, Until=self._onScopeUntil, Group=self._getScopeGroup())

        with self.tc as source:
            self._onScopeActivate(source)
            pass
        pass

    def _onScopeActivate(self, source):
        pass

    def _onDeactivate(self):
        super(BaseScopeEntity, self)._onDeactivate()

        self._onScopeDeactivate()
        self.__cancelScope()
        pass

    def _onFinalize(self):
        super(BaseScopeEntity, self)._onFinalize()

        self.__cancelScope()
        pass

    def __cancelScope(self):
        if self.tc is None:
            return

        tc = self.tc
        self.tc = None
        tc.cancel()
        pass

    def _onScopeDeactivate(self):
        pass
    pass