from Foundation.System import System

class SystemAndroidLifecycle(System):

    def _onInitialize(self):
        if _ANDROID is False:
            return

        self.__setCallbacks()

    def __setCallbacks(self):
        plugins_callbacks = {"MengineActivityLifecycle": {"onActivityLifecycleResumed": Notificator.onAndroidActivityResumed, "onActivityLifecyclePaused": Notificator.onAndroidActivityPaused, "onActivityLifecycleStarted": Notificator.onAndroidActivityStarted, "onActivityLifecycleStopped": Notificator.onAndroidActivityStopped, "onActivityLifecycleDestroyed": Notificator.onAndroidActivityDestroyed, "onActivityLifecycleCreated": Notificator.onAndroidActivityCreated,
            "onActivityLifecycleSaveInstanceState": Notificator.onAndroidActivitySaveInstanceState}}

        for plugin, plugin_callbacks in plugins_callbacks.items():
            for method, notificator in plugin_callbacks.items():
                Menge.setAndroidCallback(plugin, method, self.__createCallback(notificator))

    def __createCallback(self, notificator):
        def _cb():
            Notification.notify(notificator)

        return _cb