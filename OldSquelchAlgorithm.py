import MovingAverage
import time
import datetime

class SquelchAlgorithm:
    # take in csv files as parameters instead of the timestamp and temp?

    # assuming one data point (a temperature) taken every minute during interval length
    def __init__(self, interval_len, delta):
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
        # self.stove_on_moving_average = 0
        self.max_temp = 0
        self.max_temp_moving_average = 0 # make moving average object class

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


    # simmering
    # could update an "ON" moving average, and if the temp decreases but does not go off, that's simmering
    def update_state(self, new_temp, timestamp):
        if new_temp > self.max_temp:
            self.max_temp = new_temp
        if new_temp > self.threshold and new_temp > 3 + self.moving_average: # if large increase in temp and hot
            if self.state == 'OFF':
                self.start_time = timestamp
                self.state = 'ON'
            # create a new moving average while the stove is on, and if it drops below that, its simmering.
                # self.stove_on_moving_average = self.compute_moving_average()
        elif self.state == 'ON':
                self.times_on.append(timestamp - self.start_time)
                self.state = 'OFF'

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