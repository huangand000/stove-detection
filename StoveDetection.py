import datetime
import time

class SquelchAlgorithm:
    
    """
    A Stove Top Detection Device Microservice Helper Class.
    Utilizing fields, data sets, and measurements to calculate a moving average
    for three different types of data:
        * Ambient Temperature
        * Stove Duration Usage
        * Maximum Temperature per day
    """
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


    """
    Main function to update the information with given measurements.
    Taking in a temperature measurement, this function will update all 
    information including:
    * Stove state
    * Moving average for temperature
    * Moving average for duration of stove usage
    * Updates temperature data set
    * Updates duration data set
    * Starts/Checks timer for abnormal stove activity
    :param new_temp: A temperature measurement in Celsius
    """
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


    """
    Prints out valuable field values
    """
    def toString(self):
            print "Temperature History:", self.ambient_temp_history 
            print "Duration History:", self.duration_history
            print "Max Temperature History:", self.max_temp_history
            print "Ambient Temperature Moving Average:", self.moving_average
            print "Duration Moving Average:", self.duration_moving_average
            print "Max Temperature Moving Average:", self.max_temp_moving_average
            print "State:", self.state
            print "Max Temperature:", self.max_temp 

    """
    Private function to store stove duration of usage
    :param prev_state: Previous ON/OFF/SIMMERING state 
    :param new_temp: A temperature measurement in Celsius
    """
    def _check_and_store_duration(self, prev_state, new_temp):
        if (prev_state == "ON" and self.state == "OFF") or (prev_state == "SIMMERING" and self.state == "OFF"):
            if ("ON" in self.curr_states or "SIMMERING" in self.curr_states) and "OFF" in self.curr_states:
                on_time = datetime.datetime.strptime(self.curr_states["ON"], "%Y-%m-%d %H:%M:%S.%f")
                off_time = datetime.datetime.strptime(self.curr_states["OFF"], "%Y-%m-%d %H:%M:%S.%f")
                difference = (off_time - on_time).total_seconds()
                self.duration_moving_average = self._moving_average(self.duration_history,
                                                                    self.duration_moving_average, difference)
                self.curr_states = {}
        self.prev_temp = new_temp

    """
    Updates the max temperature moving average.
    If the stove wasn't turned on, max temp set to 0.
    """
    def check_and_store_maxTemp(self):
        if self.max_temp != 0:
            self.max_temp_moving_average = self._moving_average(self.max_temp_history, self.max_temp_moving_average,
                                                                self.max_temp)
        self.max_temp = 0

    """
    Private function to start a timer when the stove is turned on.
    """
    def _start_timer(self):
        self.timer = datetime.datetime.now()

    """
    Private function to check if the stove has been on for a abnormal duration.
    """
    def _check_timer(self):
        print "this is ",self.duration_moving_average
        if len(self.duration_history) != 0:
            if (datetime.datetime.now() - self.timer).total_seconds() > self.duration_moving_average + \
                    self.duration_delta.total_seconds():
                print "Stove been on for too long"

    """
    Private function that calculates the moving average.
    :param: data_set: A list with any numerical data
    :param: moving_average: Calculates a moving average given the data set.
    :param: data: A single numerical measurement to update the data set and moving average
    :return moving_average: Returns the updated moving average
    """
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
    sq = SquelchAlgorithm(5)
    for i in range(0,2):
        sq.update_moving_average(25)
        sq.update_moving_average(31)
        sq.update_moving_average(25)
        sq.update_moving_average(25)
        sq.update_moving_average(35)
        time.sleep(20)
        sq.update_moving_average(25)
        sq.update_moving_average(40)
        sq.update_moving_average(30)

        sq.toString()


