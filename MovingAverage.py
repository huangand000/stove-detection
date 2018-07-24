class MovingAverage:

    def __init__(self, interval_len, average=0, data=[]):
        self.interval_len = interval_len
        self.average = average
        self.data = data

    # Updates the average of this moving average object
    def update_average(self, new_value):
        if len(self.data) == self.interval_len:
            new_average = (self.average * len(self.data) + new_value - self.data[0]) / float(self.interval_len)
            self.data.pop(0)
        else:
            new_average = (self.average * len(self.data) + new_value) / float((len(self.data) + 1))
        self.data.append(new_value)
        return new_average

    if __name__ == "__main__":
        print "hi"