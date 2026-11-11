from Foundation.BaseScopeEntity import BaseScopeEntity
from Foundation.ObjectManager import ObjectManager

class MovieTabsGroup(BaseScopeEntity):
    ENTITY_SCOPE_REPEAT = True

    available_movies = ['Idle', 'Progress', 'Block', 'Idle', 'Holder']

    @staticmethod
    def declareORM(Type):
        BaseScopeEntity.declareORM(Type)

        Type.addActionActivate("Tabs")
        Type.addActionActivate("Choice", Update=Type._updateChoice)
        pass

    def _updateChoice(self, value):
        if value == self.old_choice:
            return

        new_tab = self.tabs.get(value, None)
        old_tab = self.tabs.get(self.old_choice, None)
        if new_tab is None:
            return

        new_tab[1].setEnable(False)
        new_tab[0].setEnable(True)
        self.old_choice = value

        if old_tab is not None:
            old_tab[0].setEnable(False)
            old_tab[1].setEnable(True)
        pass

    def __init__(self):
        super(MovieTabsGroup, self).__init__()

        self.tabs = {}
        self.old_choice = None
        pass

    def _onInitialize(self, obj):
        super(MovieTabsGroup, self)._onInitialize(obj)

        self.__set_tabs()
        return True

    def get_default(self):
        return self.object.getTabs()[0]

    def _getScopeGroup(self):
        return None

    def _onScopeActivate(self, source):
        for tab in self.tabs.itervalues():
            tab[1].setEnable(True)
            tab[0].setEnable(False)

        self.old_choice = self.get_default()

        self.tabs[self.old_choice][0].setEnable(True)
        self.tabs[self.old_choice][1].setEnable(False)

        for (key, value), source_slot in source.addRaceTaskList(self.tabs.iteritems()):
            source_slot.addTask("TaskMovieButtonClick", MovieButton=value[1])
            source_slot.addFunction(self.object.setParam, 'Choice', key)
            source_slot.addNotify(Notificator.onTabGroupSelect, self.object, key)
            pass
        pass

    def _onFinalize(self):
        super(MovieTabsGroup, self)._onFinalize()
        for tab in self.tabs.itervalues():
            for state in tab:
                state.getEntityNode().removeFromParent()
                state.onDestroy()

        self.tabs = {}
        pass

    def __set_tabs(self):
        for tab in self.object.getTabs():
            MovieTrueIdle = "Movie{}_{}_Down".format(self.object.getGroupName(), tab)
            MovieFalseIdle = "Movie{}_{}_Idle".format(self.object.getGroupName(), tab)

            btn_true = ObjectManager.createObjectUnique("MovieButton", '{}_Down'.format(tab), self.object,
                                                        ResourceMovieIdle=MovieTrueIdle)
            btn_false = ObjectManager.createObjectUnique("MovieButton", '{}_Idle'.format(tab), self.object,
                                                         ResourceMovieIdle=MovieFalseIdle)

            self.addChild(btn_true.getEntityNode())
            self.addChild(btn_false.getEntityNode())
            self.tabs[tab] = btn_true, btn_false

    def _onScopeDeactivate(self):
        for tab in self.tabs.itervalues():
            for state in tab:
                state.setEnable(False)
        pass