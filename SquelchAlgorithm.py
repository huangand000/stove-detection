import MovingAverage
import datetime

class SquelchAlgorithmClass:

    # assuming one data point (a temperature) taken every minute during interval length
    def __init__(self, interval_len=1, delta=3):
        self.data = []
        # self.moving_average = 0
        self.recent_temps = MovingAverage(15)
        self.state = "OFF"
        self.delta = delta
        self.times_on = []
        self.start_time = 0
        self.times_on_today = MovingAverage(20)
        self.times_on_by_day = MovingAverage(30)
        self.times_on_by_month = MovingAverage(12)
        self.max_temp = 0
        self.max_temp_moving_average = 0 # make moving average object class
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
                self.max_temp = curr_temp
        else:
            self.state = 'OFF'
            self.curr_states["OFF"] = str(datetime.datetime.now()).split('.')[0]

        if self.state == 'OFF':  # Moving average only updates if the stove is off
            self.recent_temps.update_average
        self._check_and_stove_duration(prev_state, curr_temp)

    # Need more checks: if no AC, house could be above threshold temp
    def update_moving_average(self, new_temp):
        if self.state == 'OFF': # Moving average only updates if the stove is off
            self.moving_average = self.compute_moving_average(self.data_points, new_temp, self.interval_len, self.moving_average)


    # this method should be called every 24 hours, so the max temp for a day is added to the list
    def update_max_temp_moving_average(self, new_temp, interval):
        self.max_temp_moving_average = self.compute_moving_average(self.max_temp_history, self.max_temp)
        self.max_temp = 0

    def _initial_data_gathering(self, new_temp):
        if len(self.data_points) < self.interval_len:
            self.data_points.append(new_temp)
            return

    def _check_and_stove_duration(self, curr_state, new_temp):
        if (curr_state == "ON" and self.state == "OFF") or (curr_state == "SIMMERING" and self.state == "OFF"):
            if ("ON" in self.curr_states or "SIMMERING" in self.curr_states) and "OFF" in self.curr_states:
                on_time = datetime.datetime.strptime(self.curr_states["ON"], "%Y-%m-%d %H:%M:%S")
                off_time = datetime.datetime.strptime(self.curr_states["OFF"], "%Y-%m-%d %H:%M:%S")
                self.times_on.append(on_time - off_time)
        self.prev_temp = new_temp

    # Returns the moving average of how long the stove has been on
    # def stove_time_moving_average(self):
        # also need to do this for weeks and months
        # self.stove_time_moving_average = self.compute_moving_average(self.times_on, ,)


        # flags - to be implemented by microservice. What do we need to do? Create methods that can be called to see
        # if the below conditions are true.
        #
        # Stove has been on for a while - return time - time_moving_average
        # Stove is too hot - return maxtemp - maxaveragetemp > 30
        #
    if __name__ == "__main__":
        sq = SquelchAlgorithm()