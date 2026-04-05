from Foundation.System import System


class SystemAndroid(System):
    def __init__(self):
        super(SystemAndroid, self).__init__()

        self._android_callbacks = {}

    def _addAndroidCallback(self, plugin_name, callback_name, callback):
        plugin_callbacks = self._android_callbacks.setdefault(plugin_name, {})

        if _DEVELOPMENT is True and callback_name in plugin_callbacks:
            Trace.log("System", 0, "{}: callback {!r} is already exists !!!".format(self.__class__.__name__, callback_name))

        identity = Mengine.addAndroidCallback(plugin_name, callback_name, callback)
        plugin_callbacks[callback_name] = identity
        return identity

    def _removeAndroidCallbacks(self, plugin_name=None):
        if plugin_name is None:
            for current_plugin_name in list(self._android_callbacks.keys()):
                self._removeAndroidCallbacks(current_plugin_name)
            return

        plugin_callbacks = self._android_callbacks.pop(plugin_name, {})

        for callback_name, identity in plugin_callbacks.items():
            Mengine.removeAndroidCallback(plugin_name, callback_name, identity)

    @staticmethod
    def _androidMethod(plugin_name, method_name, *args):
        return Mengine.androidMethod(plugin_name, method_name, *args)

    @staticmethod
    def _androidBooleanMethod(plugin_name, method_name, *args):
        return Mengine.androidBooleanMethod(plugin_name, method_name, *args)

    @staticmethod
    def _androidIntegerMethod(plugin_name, method_name, *args):
        return Mengine.androidIntegerMethod(plugin_name, method_name, *args)

    @staticmethod
    def _androidStringMethod(plugin_name, method_name, *args):
        return Mengine.androidStringMethod(plugin_name, method_name, *args)