from GOAP2.Params import DefaultParam

class Actor(object):
    __metaclass__ = baseslots()

    class Action(object):
        __slots__ = "events", "activate"

        def __init__(self, events, activate):
            self.events = events
            self.activate = activate
            pass
        pass

    @staticmethod
    def declareORM(typeActor):
        typeActor.actions = {}
        typeActor.actionsCache = []
        pass

    @staticmethod
    def releaseORM(typeActor):
        typeActor.actions = {}
        typeActor.actionsCache = []
        pass

    @staticmethod
    def addActionActivate(typeActor, key, **params):
        typeActor.addAction(typeActor, key, Activate=True, **params)
        pass

    @staticmethod
    def addAction(typeActor, key, Activate=False, **params):
        def __get_key(self):
            if self.object is None:
                Trace.log("Actor", 0, "Actor %s get property %s in destroy entity" % (type(self).__name__, key))

                return None
                pass

            return self.object.getParam(key)
            pass

        def __set_key(self, value):
            Trace.log("Actor", 0, "Actor %s set property read only %s (set value %s)" % (type(self).__name__, key, value))
            pass

        property_key = property(__get_key, __set_key, None, None)

        setattr(typeActor, key, property_key)

        Update = params.get("Update", None)
        Append = params.get("Append", None)
        Remove = params.get("Remove", None)
        Change = params.get("Change", None)

        InsertDict = params.get("InsertDict", None)
        PopDict = params.get("PopDict", None)

        events = dict(Update=Update, Append=Append, Remove=Remove, Change=Change, InsertDict=InsertDict, PopDict=PopDict)

        if key in typeActor.actions:
            typeActor._actorFailed(typeActor, "Actor already have action '%s'" % (key))
            return
            pass

        actions = Actor.Action(events, Activate)

        typeActor.actions[key] = actions
        typeActor.actionsCache.append((key, actions))
        pass

    def validateAction(self, params):
        keys = params.keys()
        for key in keys[:]:
            if key not in self.actions:
                typeActor = type(self)
                self._actorFailed(typeActor, "Actor invalid action '%s'" % (key))

                return False
                pass

            keys.remove(key)
            pass

        if len(keys) != 0:
            typeActor = type(self)
            self._actorFailed(typeActor, "Actor invalid action '%s'" % (keys))

            return False
            pass

        return True
        pass

    def __callAction(self, type, action, *value):
        if self._isActorValid() is False:
            Trace.log("Actor", 0, "invalid %s call action %s (Actor Invalid)" % (self, type))
            return False
            pass

        event = action.events.get(type)

        if event is None:
            return False
            pass

        if action.activate is True:
            if self._isActorActive() is False:
                return True
                pass
            pass

        event(self, *value)

        return True
        pass

    def callAction(self, key, activate, type, *value):
        if key not in self.actions:
            typeActor = type(self)
            self._actorFailed(typeActor, "Actor not have action '%s'" % (key))
            return False
            pass

        action = self.actions[key]

        if activate is True and action.activate is False:
            return True
            pass

        if self.__callAction(type, action, *value) is False:
            return False
            pass

        return True
        pass

    def callActions(self, params, activate, initialize, event):
        for key, action in self.actionsCache:
            if key not in params:
                continue
                pass

            if activate is True and action.activate is False:
                continue
                pass

            value = params[key]

            if initialize is True and isinstance(value, DefaultParam) is True:
                continue
                pass

            self.__callAction(event, action, value)
            pass
        pass

    @staticmethod
    def _actorFailed(self, typeActor, msg):
        pass

    def _isActorActive(self):
        pass

    def _isActorValid(self):
        return True
        pass
    pass