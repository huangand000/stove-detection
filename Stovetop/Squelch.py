import MovingAverage
import datetime

class Squelch:


    # We are assuming one new temperature is being taken every minute, so interval length is equal to the number of
    # temperatures being considered in the moving average
    def __init__(self, recent_temperature_interval, threshold=29, delta=3):
        self.recent_temperature = MovingAverage(recent_temperature_interval)
        self.durations_single_day = MovingAverage(20)
        self.durations_daily = MovingAverage(31)
        self.durations_monthly = MovingAverage(5)
        self.last_timestamp_turned_on = None
        self.stove_on = False
        self.daily_max_temp
        self.delta = delta
        self.months = {}

    def update_information(self, new_temp, timestamp):
        timestamp = datetime.strptime(timestamp[0:13], '%Y-%m-%dTS')
        # stove going from off to on
        if not self.stove_on and new_temp and new_temp > self.recent_temperature.average + self.delta:
            self.stove_on = True
            self.last_timestamp_turned_on = timestamp
        # stove going from on to off
        elif self.stove_on and new_temp < self.moving_average + self.delta15:
            self.stove_on = False
            self.durations_single_day.update_average((timestamp - self.last_timestamp_turned_on).total_seconds())
        if not self.stove_on:
            self.recent_temperature.update_average(new_temp)
        if self.last_timestamp_turned_on.datetime.month != timestamp.datetime.month:
            self.durations_monthly.update_average(self.durations_daily.average)
            self.durations_daily = MovingAverage(31)
            self.months.
        if self.last_timestamp_turned_on.datetime.day != timestamp.datetime.day:
            self.durations_daily.update_average(self.durations_single_day)
            self.durations_single_day = MovingAverage(10)


'[mar_avg, april_avg, may_avg...]'



