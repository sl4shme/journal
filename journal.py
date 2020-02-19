from datetime import datetime


class Day(object):
    def __init__(self, date):
        if type(date) == str:
            self.date = datetime.strptime(date, '%Y-%m-%d')
        else:
            self.date = date

        self.date_str = self.__repr__()

    def __repr__(self):
        return self.date.strftime('%Y-%m-%d')
