from Foundation.Task.MixinObserver import MixinObserver
from Foundation.Task.Task import Task


class TaskKeyPress(MixinObserver, Task):

    def onParams(self, params):
        super(TaskKeyPress, self).onParams(params)
        self.keys = params.get("Keys")
        self.add_keys = params.get('AdditionKeys', [])
        self.isDown = params.get("isDown", True)

        if self.__isIterable(self.keys, "Keys") is False:
            self.keys = [self.keys]
        if self.__isIterable(self.add_keys, "AdditionKeys") is False:
            self.add_keys = [self.add_keys]

    def __isIterable(self, param, param_name):
        if any([isinstance(param, list), isinstance(param, tuple)]) is False:
            if _DEVELOPMENT is True:
                trace_msg = "TaskKeyPress: invalid type of param {!r} - should be iterable (tuple or list). ".format(param_name)
                trace_msg += "Your input type is {}. Try to correct it making list from {!r}...".format(type(param), param)
                Trace.log("Task", 0, trace_msg)
            return False
        return True

    def _onRun(self):
        self.addObserver(Notificator.onKeyEvent, self.__onKeyEvent)
        return False

    def __onKeyEvent(self, key, x, y, isDown, isRepeating):
        for add_key in self.add_keys:
            if Mengine.isKeyDown(add_key) is False:
                return False

        if isDown is not self.isDown:
            return False

        if key not in self.keys:
            return False

        return True
