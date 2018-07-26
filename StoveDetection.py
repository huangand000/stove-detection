import datetime
import time

class SquelchAlgorithmClass:
    
    # assuming one data point (a temperature) taken every minute during interval length
    def __init__(self, interval_len = 5):
        
        # List of Ambient Temperature History
        self.ambient_temp_history = [] 
        # List of Duration History
        self.duration_history = []
        # List of Max Temperature History
        self.max_temp_history = []


        # Moving average of Ambient Temperature History
        self.moving_average = 0
        # Moving average of Max Temperature History
        self.max_temp_moving_average = 0
        # Moving average of Duration History
        self.duration_moving_average = 0


        # A set interval length for number of data points measured
        self.interval_len = interval_len

        # The state ON/OFF
        self.state = "OFF"
        # Dictionary used to track the current states
        self.curr_states = {} 
        # The current maximum temperature
        self.max_temp = 0
        # Current temperature
        self.prev_temp = None
        # Static Standard Deviation for Moving Average
        self.temp_delta = 5
        # Timer for stove when turned on
        self.timer = datetime.datetime.now()
        # Static Standard Deviation for Duration time
        self.duration_delta = datetime.timedelta(seconds = 10)



    def update_moving_average(self, new_temp):
        if len(self.ambient_temp_history) == 0:
            self.moving_average = new_temp
        prev_state = self.state
        if new_temp > self.temp_delta + self.moving_average: # if hot and large increase in temp
            self._start_timer()
            self.state = 'ON'
            self.curr_states["ON"] = str(datetime.datetime.now())
            if new_temp < self.prev_temp:
                self.state = 'SIMMERING'
                self.curr_states["SIMMERING"] = str(datetime.datetime.now())
            if new_temp > self.max_temp:
                self.max_temp = new_temp
                self.check_and_store_maxTemp()
        else:
            self.state = 'OFF'
            self.curr_states["OFF"] = str(datetime.datetime.now())

        if self.state == 'OFF': # Moving average only updates if the stove is off
            self.moving_average = self._moving_average(self.ambient_temp_history, self.moving_average, new_temp)
        self._check_and_store_duration(prev_state, new_temp)
        self._check_timer()


        
    def toString(self):
            print "Temperature History:", self.ambient_temp_history 
            print "Duration History:", self.duration_history
            print "Max Temperature History:", self.max_temp_history
            print "Ambient Temperature Moving Average:", self.moving_average
            print "Duration Moving Average:", self.duration_moving_average
            print "Max Temperature Moving Average:", self.max_temp_moving_average
            print "State:", self.state
            print "Max Temperature:", self.max_temp 

    def _check_and_store_duration(self, prev_state, new_temp):
        if (prev_state == "ON" and self.state == "OFF") or (prev_state == "SIMMERING" and self.state == "OFF"):
            if ("ON" in self.curr_states or "SIMMERING" in self.curr_states) and "OFF" in self.curr_states:
                on_time = datetime.datetime.strptime(self.curr_states["ON"], "%Y-%m-%d %H:%M:%S.%f")
                off_time = datetime.datetime.strptime(self.curr_states["OFF"], "%Y-%m-%d %H:%M:%S.%f")
                self.duration_history.append(off_time - on_time)
                self._set_duration_moving_average()
                self.curr_states = {}
        self.prev_temp = new_temp

    # Calculates the moving average for the time the stove has been on
    def _set_duration_moving_average(self):
        if len(self.duration_history) == self.interval_len + 1:
            self.duration_history.pop(0) # if duration_history is longer than the interval, remove the first value
       
        total = datetime.timedelta(seconds = 0)
        for time in self.duration_history:
            total += time
        self.duration_moving_average = total / len(self.duration_history)


    # updates the max temp moving average if the stove was on since the last update, resets max_temp
    def check_and_store_maxTemp(self):
        if self.max_temp != 0:
            self.max_temp_moving_average = self._moving_average(self.max_temp_history, self.max_temp_moving_average, self.max_temp)
        self.max_temp = 0

    def _start_timer(self):
        self.timer = datetime.datetime.now()

    def _check_timer(self):
        print "this is ",self.duration_moving_average
        if len(self.duration_history) != 0:
            if (datetime.datetime.now() - self.timer) > self.duration_moving_average + self.duration_delta: 
                print "Stove been on for too long"

    # Combine algorithm of calcuating moving average for temp, duration, and max_temp
    def _moving_average(self, data_set, moving_average, data):
        if len(data_set) == self.interval_len:
            moving_average = (moving_average * len(data_set) + 
                                   data - data_set[0]) / self.interval_len
            data_set.pop(0)
        else:
            moving_average = (moving_average * len(data_set) + 
                                   data) / (len(data_set) + 1)
        data_set.append(data)
        return moving_average


        

    
if __name__ == "__main__":
    sq = SquelchAlgorithmClass(5)
    for i in range(0,2):
        sq.update_moving_average(25)
    sq.update_moving_average(31)
    sq.update_moving_average(25)
    sq.update_moving_average(25)
    sq.update_moving_average(35)
    sq.update_moving_average(25)
    sq.update_moving_average(40)
    sq.update_moving_average(30)




    sq.toString()


