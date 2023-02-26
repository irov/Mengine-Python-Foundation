from Task import Task

class TaskVirtualAreaScroll(Task):
    def __init__(self):
        super(TaskVirtualAreaScroll, self).__init__()
        self.progress_value_follower_x = None
        self.progress_value_follower_y = None

    def _onParams(self, params):
        super(TaskVirtualAreaScroll, self)._onParams(params)

        self.virtual_area = params.get('VirtualArea', None)
        self.current_value = params.get('current_percent', None)
        self.finish_value = params.get('finish_percent', None)
        self.time = params.get("Time", None)
        self.speed = params.get("Speed", None)

        self.wait = params.get("Wait", False)

    def __update_x(self, new_value, virtual_area):
        virtual_area.set_percentage(x=new_value)
        if new_value == self.finish_value.x:
            Menge.destroyValueFollower(self.progress_value_follower_x)
            if self.wait is True:
                self.complete()

    def __update_y(self, new_value, virtual_area):
        virtual_area.set_percentage(y=new_value)
        if new_value == self.finish_value.y:
            Menge.destroyValueFollower(self.progress_value_follower_y)
            if self.wait is True:
                self.complete()

    def _onFastSkip(self):
        self.virtual_area.set_percentage(x=self.finish_value[0], y=self.finish_value[1])
        return True

    def _onRun(self):
        super(TaskVirtualAreaScroll, self)._onRun()

        current_percent_value = self.virtual_area.get_percentage()
        if self.current_value is None:
            self.current_value = current_percent_value
        else:
            self.virtual_area.set_percentage(x=self.current_value[0], y=self.current_value[1])

        finish_value = [self.finish_value[0], self.finish_value[1]]
        for dim in range(2):
            if self.finish_value[dim] is None:
                finish_value[dim] = current_percent_value[dim]

        self.current_value = Menge.vec2f(self.current_value[0], self.current_value[1])
        self.finish_value = Menge.vec2f(finish_value[0], finish_value[1])

        if self.speed is None:
            value_offset = Menge.length_v2_v2(self.current_value, self.finish_value)
            self.speed = float(value_offset) / float(self.time)

        if self.current_value.x != self.finish_value.x:
            self.progress_value_follower_x = Menge.createValueFollowerLinear(self.current_value.x, self.speed, self.__update_x, self.virtual_area)

        if self.current_value.y != self.finish_value.y:
            self.progress_value_follower_y = Menge.createValueFollowerLinear(self.current_value.y, self.speed, self.__update_y, self.virtual_area)  # print "----- y =", self.current_value.y, "speed =", self.speed

        if all([self.current_value.x == self.finish_value.x, self.current_value.y == self.finish_value.y]):
            return True
        if self.progress_value_follower_x:
            self.progress_value_follower_x.setFollow(self.finish_value.x)
        if self.progress_value_follower_y:
            self.progress_value_follower_y.setFollow(self.finish_value.y)

        if self.wait:
            return False

        return True

    def _onCheck(self):
        if all([self.virtual_area is None, self.time is None and self.speed is None, self.finish_value is None]):
            return False
        return True

    def _onFinalize(self):
        super(TaskVirtualAreaScroll, self)._onFinalize()