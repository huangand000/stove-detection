import datetime
import time

class StoveDetection:
    
    # assuming one data point (a temperature) taken every minute during interval length
    def __init__(self, interval_len):
        # A list used to capture a set length of data points
        self.data_points = [] 
        # A dynamic moving/running average of the data points
        self.moving_average = 0
        # A set internal length for number of data points captured for moving/running average
        self.interval_len = interval_len
        # The state ON/OFF
        self.state = "OFF"
        # dictionary, can also be used for finding running average of total time
        self.state_history = []
        # Dictionary used to track the current states
        self.curr_states = {} 
        # The current maximum temperature
        self.max_temp = 0
        # Current temperature
        self.curr_temp = None
        self.temp_delta = 3
        self.duration_delta = datetime.timedelta(seconds = 30)
        # Moving average for the time the stove has been on
        self.duration_moving_average = 0
        # Timer for stove when turned on
        self.timer = datetime.datetime.now()

        """" new fields for max temp """""
        self.max_temp_list = []
        self.max_temp_moving_average = 0
        self.max_temp_interval_len = 30

        """" new fields for max temp """


    def update_moving_average(self, new_temp):
        if len(self.data_points) == 0:
            self.moving_average = new_temp
        curr_state = self.state
        if new_temp > self.temp_delta + self.moving_average: # if hot and large increase in temp
            self.state = 'ON'
            self._start_timer()
            self.curr_states["ON"] = str(datetime.datetime.now())
            if new_temp < self.curr_temp:
                self.state = 'SIMMERING'
                self.curr_states["SIMMERING"] = str(datetime.datetime.now())
            if new_temp > self.max_temp:
                self.max_temp = new_temp
        else:
            self.state = 'OFF'
            self.curr_states["OFF"] = str(datetime.datetime.now())

        if self.state == 'OFF': # Moving average only updates if the stove is off
            if len(self.data_points) == self.interval_len:
                self.moving_average = (self.moving_average * len(self.data_points) + new_temp - self.data_points[0]) / self.interval_len
                self.data_points.pop(0)
            else:
                self.moving_average = (self.moving_average * len(self.data_points) + new_temp) / (len(self.data_points) + 1)
            self.data_points.append(new_temp)
        self._check_and_store_duration(curr_state, new_temp)
        self._check_timer()

        
    def toString(self):
            print "Data Points:", self.data_points 
            print "Moving Average:", self.moving_average
            print "Interval Length:", self.interval_len
            print "State:", self.state
            print "Current States", self.curr_states 
            print "State History", self.state_history
            print "Max Temperature:", self.max_temp 
            print "Last record Temperature:", self.curr_temp
            print "Timer:", self.timer

    def _check_and_store_duration(self, curr_state, new_temp):
        if (curr_state == "ON" and self.state == "OFF") or (curr_state == "SIMMERING" and self.state == "OFF"):
            if ("ON" in self.curr_states or "SIMMERING" in self.curr_states) and "OFF" in self.curr_states:
                on_time = datetime.datetime.strptime(self.curr_states["ON"], "%Y-%m-%d %H:%M:%S.%f")
                off_time = datetime.datetime.strptime(self.curr_states["OFF"], "%Y-%m-%d %H:%M:%S.%f")
                self.state_history.append(off_time - on_time)
                self.set_duration_moving_average()
        self.curr_temp = new_temp

    # Calculates the moving average for the time the stove has been on
    def _set_duration_moving_average(self):
        if len(self.state_history) == self.interval_len + 1:
            self.state_history.pop(0) # if state_history is longer than the interval, remove the first value
        total = 0
        for time in self.state_history:
            total += time
        self.duration_moving_average = float(total) / len(self.state_history)

    def _start_timer(self):
        self.timer = datetime.datetime.now()

    def _check_timer(self):
        if len(self.state_history) > 0:
            # Use state moving average to determine instead of looping through state_history
            for state in self.state_history:
                print "Timer now: ", datetime.datetime.now() - self.timer
                print state
                if (datetime.datetime.now() - self.timer) > state + self.duration_delta: 
                    print "Stove been on for too long"

    # updates the max temp moving average if the stove was on since the last update, resets max_temp
    def _check_and_store_maxTemp(self):
        """
        Andre's Comments:
        * If max_temp is being set to 0 every time at the end of the method, how are we getting 
            the max temp for that day? 
        * See if you can make the max_temp_list keep track of a max temp of each day 
            (could have multiple uses of stove per day, only want max temp of that day).
        """
        if self.max_temp != 0:
            self.max_temp_list.append(self.max_temp)
            if len(self.max_temp_list) == self.max_temp_interval_len:
                self.max_temp_moving_average = (self.max_temp_moving_average * len(self.max_temp_list) +
                                                self.max_temp - self.max_temp_list[0]) / self.max_temp_interval_len
                self.max_temp_list.pop(0)
            else:
                self.max_temp_moving_average = (self.max_temp_moving_average * len(self.max_temp_list)
                                                + self.max_temp) / (len(self.max_temp_list) + 1)
            self.data_points.append(self.max_temp)
        self.max_temp = 0

    # Combine algorithm of calcuating moving average for temp, duration, and max_temp
    def _moving_average(self):
        pass

"""
if __name__ == "__main__":
    for i in range(0,2):
        sq.update_moving_average(25)
    sq.update_moving_average(30)
    sq.update_moving_average(25)
    sq.update_moving_average(25)
    sq.update_moving_average(35)
    time.sleep(32)
    sq.update_moving_average(25)


    sq.toString()
"""

""" 
TO-DO LIST

Liam: 
* Create a moving average for duration
* Update the state history list with durations retrieved from _check_and_store_duration()

Ryan: 
* Create a moving average for max temp
* Update a max temp history list and method that can _check_and_store_maxTemp()
"""
