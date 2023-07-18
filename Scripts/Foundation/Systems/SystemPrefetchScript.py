from Foundation.System import System


class SystemPrefetchScript(System):
    def _onRun(self):
        self.addObserver(Notificator.onInitializeRenderResources, self.__prefetchScripts)
        return True

    def __prefetchScripts(self):
        def __cb(result):
            if _DEVELOPMENT is True:
                Trace.msg("SystemPrefetchScript prefetch result: {}".format(result))

        Mengine.prefetchScripts(__cb)
        return True
