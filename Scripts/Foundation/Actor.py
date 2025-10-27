from Foundation.Params import DefaultParam
from Foundation.Params import ParamsException

class Actor(object):
    __metaclass__ = baseslots()

    class Action(object):
        __slots__ = "Update", "Append", "Remove", "Change", "InsertDict", "PopDict", "Activate"

        def __init__(self, Params, Activate):
            self.Update = Params.get("Update", None)
            self.Append = Params.get("Append", None)
            self.Remove = Params.get("Remove", None)
            self.Change = Params.get("Change", None)
            self.InsertDict = Params.get("InsertDict", None)
            self.PopDict = Params.get("PopDict", None)

            self.Activate = Activate
            pass
        pass

    @staticmethod
    def declareORM(typeORM):
        typeORM.ACTOR_ACTIONS = {}
        typeORM.ACTOR_ACTIONS_CACHE = []
        pass

    @classmethod
    def addActionActivate(cls, key, **Params):
        cls.addAction(key, Activate=True, **Params)
        pass

    @classmethod
    def addAction(cls, key, Activate=False, **Params):
        if _DEVELOPMENT is True:
            def __get_key(self):
                if self.object is None:
                    Trace.log("Actor", 0, "Actor %s get property %s in destroy entity" % (cls.__name__, key))

                    return None

                return self.object.getParam(key)

            def __set_key(self, value):
                Trace.log("Actor", 0, "Actor %s set property read only %s (set value %s)" % (cls.__name__, key, value))
                pass

            property_key = property(__get_key, __set_key, None, None)
        else:
            def __get_key(self):
                return self.object.getParam(key)

            property_key = property(__get_key, None, None, None)
            pass

        setattr(cls, key, property_key)

        if _DEVELOPMENT is True:
            if key in cls.ACTOR_ACTIONS:
                raise ParamsException("Actor '%s' already have action '%s' [%s]" % (cls.__name__, key, cls.ACTOR_ACTIONS[key]))

        action = Actor.Action(Params, Activate)

        cls.ACTOR_ACTIONS[key] = action
        cls.ACTOR_ACTIONS_CACHE.append((key, action))
        pass

    def validateAction(self, params):
        validate_actions = self.ACTOR_ACTIONS.keys()
        for action in validate_actions[:]:
            if action not in params:
                typeActor = type(self)
                self._actorFailed(typeActor, "Actor invalid action '%s'"%(action))

                return False

            validate_actions.remove(action)
            pass

        return True

    def __callAction(self, activate, ActionActivate, ActionEvent, *args):
        if ActionEvent is None:
            return

        if activate is True and ActionActivate is False:
            return

        if ActionActivate is True:
            if self._isActorActive() is False:
                return

        ActionEvent(self, *args)

    def callUpdateAction(self, key, activate, value):
        if _DEVELOPMENT is True:
            if self._isActorValid() is False:
                Trace.log("Actor", 0, "invalid %s call action Update '%s' (Actor Invalid)" % (self, key))
                return

            if key not in self.ACTOR_ACTIONS:
                typeActor = type(self)
                self._actorFailed(typeActor, "Actor not have action '%s'" % (key))
                return

        action = self.ACTOR_ACTIONS[key]

        self.__callAction(activate, action.Activate, action.Update, value)

        return True

    def callAppendAction(self, key, activate, index, value):
        if _DEVELOPMENT is True:
            if self._isActorValid() is False:
                Trace.log("Actor", 0, "invalid %s call action Append '%s' (Actor Invalid)" % (self, key))
                return

            if key not in self.ACTOR_ACTIONS:
                typeActor = type(self)
                self._actorFailed(typeActor, "Actor not have action '%s'" % (key))
                return

        action = self.ACTOR_ACTIONS[key]

        self.__callAction(activate, action.Activate, action.Append, index, value)

    def callRemoveAction(self, key, activate, index, value, old):
        if _DEVELOPMENT is True:
            if self._isActorValid() is False:
                Trace.log("Actor", 0, "invalid %s call action Remove '%s' (Actor Invalid)" % (self, key))
                return

            if key not in self.ACTOR_ACTIONS:
                typeActor = type(self)
                self._actorFailed(typeActor, "Actor not have action '%s'" % (key))
                return

        action = self.ACTOR_ACTIONS[key]

        self.__callAction(activate, action.Activate, action.Remove, index, value, old)

        return True

    def callChangeAction(self, key, activate, index, value):
        if _DEVELOPMENT is True:
            if self._isActorValid() is False:
                Trace.log("Actor", 0, "invalid %s call action Change '%s' (Actor Invalid)" % (self, key))
                return

            if key not in self.ACTOR_ACTIONS:
                typeActor = type(self)
                self._actorFailed(typeActor, "Actor not have action '%s'" % (key))
                return

        action = self.ACTOR_ACTIONS[key]

        self.__callAction(activate, action.Activate, action.Change, index, value)

        return True

    def callInsertDictAction(self, key, activate, dict_key, dict_value):
        if _DEVELOPMENT is True:
            if self._isActorValid() is False:
                Trace.log("Actor", 0, "invalid %s call action InsertDict '%s' (Actor Invalid)" % (self, key))
                return

            if key not in self.ACTOR_ACTIONS:
                typeActor = type(self)
                self._actorFailed(typeActor, "Actor not have action '%s'" % (key))
                return

        action = self.ACTOR_ACTIONS[key]

        self.__callAction(activate, action.Activate, action.InsertDict, dict_key, dict_value)

        return True

    def callPopDictAction(self, key, activate, dict_key, dict_value):
        if _DEVELOPMENT is True:
            if self._isActorValid() is False:
                Trace.log("Actor", 0, "invalid %s call action PopDict '%s' (Actor Invalid)" % (self, key))
                return

            if key not in self.ACTOR_ACTIONS:
                typeActor = type(self)
                self._actorFailed(typeActor, "Actor not have action '%s'" % (key))
                return

        action = self.ACTOR_ACTIONS[key]

        self.__callAction(activate, action.Activate, action.PopDict, dict_key, dict_value)

        return True

    def callUpdateActions(self, params, activate, initialize):
        if _DEVELOPMENT is True:
            if self._isActorValid() is False:
                Trace.log("Actor", 0, "invalid %s call action Updates (Actor Invalid)" % (self))
                return False

        for key, action in self.ACTOR_ACTIONS_CACHE:
            if action.Update is None:
                continue

            if activate is True and action.Activate is False:
                continue

            if key not in params:
                continue

            value = params[key]

            if initialize is True and isinstance(value, DefaultParam) is True:
                continue

            if action.Activate is True:
                if self._isActorActive() is False:
                    continue

            action.Update(self, value)
            pass
        pass

    def _actorFailed(self, typeActor, msg):
        pass

    def _isActorActive(self):
        pass

    def _isActorValid(self):
        return True