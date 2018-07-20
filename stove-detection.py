import datetime
import time
class SquelchAlgorithmClass:
    
    # assuming one data point (a temperature) taken every minute during interval length
    def __init__(self, interval_len, threshold=29):
        # A list used to capture a set length of data points
        self.data_points = [] 
        # A dynamic moving/running average of the data points
        self.moving_average = 0
        # A set internal length for number of data points captured for moving/running average
        self.interval_len = interval_len
        # The state ON/OFF
        self.state = "OFF"
        # A set temperature threshold, DEFAULT = 29 Celsius
        self.threshold = threshold 
        # dictionary, can also be used for finding running average of total time
        self.state_history = {}
        # Dictionary used to track the current states
        self.curr_states = {} 
        # The current maximum temperature
        self.max_temp = 0
        # Current temperature
        self.curr_temp = None

    # Need more checks: if no AC, house could be above threshold temp
    def update_moving_average(self, new_temp):
        self._initial_data_gathering(new_temp)
        curr_state = self.state
        if new_temp > self.threshold and new_temp > 3 + self.moving_average: # if hot and large increase in temp
            self.state = 'ON'
            self.curr_states["ON"] = str(datetime.datetime.now()).split('.')[0]
            if new_temp < self.curr_temp:
                self.state = 'SIMMERING'
                self.curr_states["SIMMERING"] = str(datetime.datetime.now()).split('.')[0]
            if new_temp > self.max_temp:
                self.max_temp = new_temp
        else:
            self.state = 'OFF'
            self.curr_states["OFF"] = str(datetime.datetime.now()).split('.')[0]

        if self.state == 'OFF': # Moving average only updates if the stove is off
            if len(self.data_points) == self.interval_len:
                self.moving_average = (self.moving_average * len(self.data_points) + new_temp - self.data_points[0]) / self.interval_len
                self.data_points.pop(0)
            else:
                self.moving_average = (self.moving_average * len(self.data_points) + new_temp) / len(self.data_points)
            self.data_points.append(new_temp)
        self._check_and_stove_duration(curr_state, new_temp)
        
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
            
    def _initial_data_gathering(self, new_temp):
        if len(self.data_points) < self.interval_len:
            self.data_points.append(new_temp)
            return

    def _check_and_stove_duration(self, curr_state, new_temp):
        if (curr_state == "ON" and self.state == "OFF") or (curr_state == "SIMMERING" and self.state == "OFF"):
            if ("ON" in self.curr_states or "SIMMERING" in self.curr_states) and "OFF" in self.curr_states:
                on_time = datetime.datetime.strptime(self.curr_states["ON"], "%Y-%m-%d %H:%M:%S")
                off_time = datetime.datetime.strptime(self.curr_states["OFF"], "%Y-%m-%d %H:%M:%S")
                if "stove_duration" not in self.state_history:
                    self.state_history["stove_duration"] = []
                self.state_history["stove_duration"].append(on_time - off_time)
        self.curr_temp = new_temp

    # Returns the moving average of how long the stove has been on
    def _moving_average_time(self):
        # total_time = 0
        # num_times = 0
        # for key in self.curr_states.keys():
                # if self.curr_states[key] == 'ON':
        return

if __name__ == "__main__":
    sq = SquelchAlgorithmClass(5)
    for i in range(0,5):
        sq.update_moving_average(25)

    sq.update_moving_average(46)
    sq.update_moving_average(25)
    sq.toString()