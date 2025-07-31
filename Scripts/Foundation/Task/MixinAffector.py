from Foundation.Task.Task import Task

class MixinAffector(Task):
    def __init__(self):
        super(MixinAffector, self).__init__()

        self.__affector = None
        self._affector_time_elapsed = 0.0

    def _Affector(self, delta_time):
        return False

    def _runAffector(self):
        def __Affector(delta_time):
            self._affector_time_elapsed += delta_time

            return self._Affector(delta_time)

        self.__affector = Mengine.addAffector(__Affector)

    def _stopAffector(self):
        """
        No need to call it explicitly in child classes in most cases
        """

    def _onFinally(self):
        super(MixinAffector, self)._onFinally()

        if self.__affector is not None:
            Mengine.removeAffector(self.__affector)
            self.__affector = None
            pass
        pass