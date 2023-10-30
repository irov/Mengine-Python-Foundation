from Foundation.System import System


# todo: delete system
class SystemAndroidLifecycle(System):

    def _onInitialize(self):
        if _ANDROID is False:
            return

        self.__setCallbacks()

    def __setCallbacks(self):
        plugins_callbacks = {}

        for plugin, plugin_callbacks in plugins_callbacks.items():
            for method, notificator in plugin_callbacks.items():
                Mengine.setAndroidCallback(plugin, method, self.__createCallback(notificator))

    def __createCallback(self, notificator):
        def _cb():
            Notification.notify(notificator)

        return _cb
