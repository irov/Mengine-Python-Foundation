from Foundation.Initializer import Initializer

class AnimatorEasing(Initializer):
    def __init__(self, pos_setter=None, start_pos=0.0, easing=0.05, time_out=10.0, epsilon=0.1):
        super(AnimatorEasing, self).__init__()
        self.cur_pos = start_pos
        self.target_pos = start_pos

        self.easing = easing
        self.time_out = time_out

        self._pos_setter = pos_setter
        self._schedule_id = None

        self._is_stop = True

        self.epsilon = epsilon

    def __update(self):
        delta = (self.target_pos - self.cur_pos) * self.easing

        if abs(delta) < self.epsilon:
            self._schedule_id = None
            self._is_stop = True
            return

        self.cur_pos += delta
        self._pos_setter(self.cur_pos)

        self._run()

    def __on_schedule(self, id_, is_complete):
        if id_ != self._schedule_id:
            return

        self.__update()

    def set_pos(self, next_pos):
        if self.cur_pos == next_pos:
            return

        self.target_pos = next_pos

        if self._is_stop:
            self._run()

    def _run(self):
        self._schedule_id = Menge.schedule(self.time_out, self.__on_schedule)

    def _stop(self):
        if self._schedule_id:
            Menge.scheduleRemove(self._schedule_id)
            self._schedule_id = None

        self._is_stop = True

    def _onInitialize(self):
        if self._pos_setter is None:
            self.initializeFailed("position setter is None")

        self._pos_setter(self.cur_pos)

    def _onFinalize(self):
        self._stop()