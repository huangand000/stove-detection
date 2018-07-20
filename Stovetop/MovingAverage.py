class MovingAverage:
    def __init__(self, interval, average=0, data=[]):
        self.interval = interval
        self.average = average
        self.data = data

    def update_average(self, new_value):
        if len(self.data) == self.interval:
            self.average = (self.average * len(self.data) - self.data[0] + new_value) / float(self.interval)
            self.data.pop(0)
        else:
            self.average = (self.average * len(self.data) + new_value) / float(len(self.data) + 1.0)
        self.data.append(new_value)

