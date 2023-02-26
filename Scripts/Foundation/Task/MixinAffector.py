import Menge
from Foundation.Task.Task import Task

class MixinAffector(Task):
    def __init__(self):
        super(MixinAffector, self).__init__()

        self.__affector_id = None
        self._affector_time_elapsed = 0.0

    def _onFinally(self):
        super(MixinAffector, self)._onFinally()
        self._stopAffector()

    def _Affector(self, delta_time):
        return False

    def __Affector(self, delta_time):
        self._affector_time_elapsed += delta_time

        return self._Affector(delta_time)

    def _runAffector(self):
        self.__affectorId = Menge.addAffector(self.__Affector)

    def _stopAffector(self):
        """
        No need to call it explicitly in child classes in most cases
        """
        if self.__affector_id is not None:
            Menge.removeAffector(self.__affectorId)
            self.__affectorId = None