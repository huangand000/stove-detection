import MovingAverage
import datetime

class SquelchAlgorithm:

    # TODO: How often to update/how long to keep track of moving averages of stove duration and max temp

    def __init__(self, interval_len, delta):
        self.recent_temps = MovingAverage(interval_len) # A moving average of the stove temperature (while off)
        self.state = "OFF" # State of the stove (OFF, ON, or SIMMERING)
        self.delta = delta # Minimum difference for a sudden large change in temp
        self.times_on = [] # A list containing the periods of time that the stove has been on recently
        self.stove_duration = MovingAverage(30) # Moving average of the time the stove is on
        self.max_temp_today = 0 # The max temperature of the stove today
        self.max_temp = MovingAverage(30) # Moving average of the max temp of the stove
        self.prev_temp = None # The previously recorded temp of the stove

    # Updates the state of the stove, and the moving average if the stove is off
    def update_state(self, curr_temp):
        # self._initial_data_gathering(curr_temp)
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


    # Should only be updated if the stove has been turned on today (if max_temp_today > some threshold temp)
    # Updates the moving average of the max temp of the stove and resets max_temp_today to 0
    def update_max_temp_moving_average(self):
        self.max_temp.update_average(self.max_temp_today)
        self.max_temp_today = 0


    # Checks to see if the stove was on and is now off, and updates the moving average of the stove duration.
    def _check_and_stove_duration(self, curr_state, curr_temp):
        if (curr_state == "ON" and self.state == "OFF") or (curr_state == "SIMMERING" and self.state == "OFF"):
            if ("ON" in self.curr_states or "SIMMERING" in self.curr_states) and "OFF" in self.curr_states:
                on_time = datetime.datetime.strptime(self.curr_states["ON"], "%Y-%m-%d %H:%M:%S")
                off_time = datetime.datetime.strptime(self.curr_states["OFF"], "%Y-%m-%d %H:%M:%S")
                self.stove_duration.update_average(on_time - off_time)
        self.prev_temp = curr_temp


    # This method may not be necessary because of the moving average class.
    # Adds the current temp to the data
    # def _initial_data_gathering(self, curr_temp):
        # if len(self.data_points) < self.interval_len:
            # self.data_points.append(curr_temp)

    # Need to update testing methods 
    def toString(self):
        print "Data Points:", self.data_points
        print "Moving Average:", self.moving_average
        print "Interval Length:", self.interval_len
        print "State:", self.state
        print "Threshold:", self.threshold
        print "Current States", self.curr_states
        print "State History", self.state_history["stove_duration"]
        print "Max Temperature:", self.max_temp
        print "Last record Temperature:", self.curr_temp


    if __name__ == "__main__":
        sq = SquelchAlgorithm(5)
        for i in range(0, 5):
            sq.update_moving_average(25)

        sq.update_moving_average(46)
        sq.update_moving_average(25)
        sq.toString()