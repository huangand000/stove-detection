import MovingAverage
import datetime

class SquelchAlgorithm:


    # assuming one data point (a temperature) taken every minute during interval length
    def __init__(self, interval_len, delta):
        self.recent_temps = MovingAverage(interval_len)
        self.state = "OFF"
        self.delta = delta
        self.times_on = []
        self.stove_duration = MovingAverage(30)
        self.max_temp_today = 0
        self.max_temp = MovingAverage(30)
        self.prev_temp = None


    def update_state(self, curr_temp):
        self._initial_data_gathering(curr_temp)
        prev_state = self.state
        if curr_temp > self.threshold and curr_temp > self.delta + self.moving_average:  # if hot and large increase in temp
            self.state = 'ON'
            self.curr_states["ON"] = str(datetime.datetime.now()).split('.')[0]
            if curr_temp < self.prev_temp:
                self.state = 'SIMMERING'
                self.curr_states["SIMMERING"] = str(datetime.datetime.now()).split('.')[0]
            if curr_temp > self.max_temp:
                self.max_temp_today = curr_temp
        else:
            self.state = 'OFF'
            self.curr_states["OFF"] = str(datetime.datetime.now()).split('.')[0]

        if self.state == 'OFF':  # Moving average only updates if the stove is off
            self.recent_temps.update_average
        self._check_and_stove_duration(prev_state, curr_temp)

    # how often should this be called
    def update_max_temp_moving_average(self):
        self.max_temp.update_average()
        self.max_temp_today = 0

    def _check_and_stove_duration(self, curr_state, new_temp):
        if (curr_state == "ON" and self.state == "OFF") or (curr_state == "SIMMERING" and self.state == "OFF"):
            if ("ON" in self.curr_states or "SIMMERING" in self.curr_states) and "OFF" in self.curr_states:
                on_time = datetime.datetime.strptime(self.curr_states["ON"], "%Y-%m-%d %H:%M:%S")
                off_time = datetime.datetime.strptime(self.curr_states["OFF"], "%Y-%m-%d %H:%M:%S")
                self.times_on.append(on_time - off_time)
        self.prev_temp = new_temp


    def _initial_data_gathering(self, new_temp):
        if len(self.data_points) < self.interval_len:
            self.data_points.append(new_temp)