from GOAP2.Task.MixinAffector import MixinAffector
from GOAP2.Task.MixinObjectTemplate import MixinMovie2
from GOAP2.Task.MixinTime import MixinTime

from Task import Task

class TaskMovie2LayerAlphaTo(MixinMovie2, MixinTime, MixinAffector, Task):
    Skiped = True
    MixinTime_Validate_TimeZero = False

    def _onParams(self, params):
        super(TaskMovie2LayerAlphaTo, self)._onParams(params)

        self.alpha_from = params.get("From", None)
        self.alpha_to = params.get("To")

        self.layer_name = params.get("Layer", None)
        self.__current_alpha = None

    def _onValidate(self):
        super(TaskMovie2LayerAlphaTo, self)._onValidate()

        if self.layer_name is None:
            self.validateFailed("layer_name is None")

    def _onInitialize(self):
        super(TaskMovie2LayerAlphaTo, self)._onInitialize()

    def _Affector(self, delta_time):
        """
        Linear interpolate layer alpha from self.alpha_from to self.alpha_to with time=self.time
        """

        delta_time_normalized = self._affector_time_elapsed / self.time
        if delta_time_normalized > 1.0:  # clamp
            delta_time_normalized = 1.0

        alpha_lerp = self.alpha_from + (self.alpha_to - self.alpha_from) * delta_time_normalized
        self.Movie2.setLayerExtraOpacity(self.layer_name, alpha_lerp)

        # check complete:
        if alpha_lerp == self.alpha_to:
            self.complete(isSkiped=False)
            return True

        if not self.Movie2.isActive():
            self.complete(isSkiped=True)
            return True

        return False

    def __onComplete(self):
        self.Movie2.setLayerExtraOpacity(self.layer_name, self.alpha_to)

    def _onRun(self):
        if self.time == 0.0:
            self.__onComplete()
            return

        if self.alpha_from is not None:
            self.Movie2.setLayerExtraOpacity(self.layer_name, self.alpha_from)

        self._runAffector()

        return False

    def _onSkip(self):
        self.__onComplete()

    def _onComplete(self):
        self.__onComplete()
        return True