from Foundation.System import System


class SystemPrefetchFont(System):
    def _onRun(self):
        self.addObserver(Notificator.onInitializeRenderResources, self.__prefetchFonts)
        self.addObserver(Notificator.onFinalizeRenderResources, self.__unfetchFonts)
        return True

    def __prefetchFonts(self):
        def __cb(result):
            if _DEVELOPMENT is True:
                Trace.msg("SystemPrefetchFont prefetch result: {}".format(result))

        Mengine.prefetchFonts(__cb)
        return True

    def __unfetchFonts(self):
        Mengine.unfetchFonts()
        return True
