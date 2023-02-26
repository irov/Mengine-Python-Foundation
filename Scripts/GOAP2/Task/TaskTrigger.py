from GOAP2.Task.Task import Task

class TaskTrigger(Task):
    Skiped = False

    def _onParams(self, params):
        super(TaskTrigger, self)._onParams(params)

        self.Trigger = params.get("Trigger")
        self.Enter = params.get("Enter", True)
        self.IFF = params.get("IFF", (0))

        self.Filter = Utils.make_functor(params, "Filter")
        pass

    def __onTriggerEnter(self, element, iff, enemy_iff):
        if enemy_iff not in self.IFF:
            return
            pass

        if self.Filter is not None:
            enemy = element.getActorUserData()

            if self.Filter(enemy, enemy_iff, iff) is False:
                return
                pass
            pass

        self.complete()
        pass

    def __onTriggerLeave(self, element, iff, enemy_iff):
        if enemy_iff not in self.IFF:
            return
            pass

        if self.Filter is not None:
            enemy = element.getActorUserData()

            if self.Filter(enemy, enemy_iff, iff) is False:
                return
                pass
            pass

        self.complete()
        pass

    def _onRun(self):
        if self.Enter is True:
            self.Trigger.setEventListener(onTriggerEnter=self.__onTriggerEnter)
            pass
        else:
            self.Trigger.setEventListener(onTriggerLeave=self.__onTriggerLeave)
            pass

        return False
        pass
    pass