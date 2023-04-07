import calendar
from datetime import datetime as dt


class Calc:
    quarter = {
        1: [dt(2023, 1, 1), dt(2023, 3, 31)],
        2: [dt(2023, 4, 1), dt(2023, 6, 30)],
        3: [dt(2023, 7, 1), dt(2023, 9, 30)],
        4: [dt(2023, 10, 1), dt(2023, 12, 31)]
    }

    year = {
        2023: {'ФОМС': 9119, 'ПФР': 36723}
    }

    def __init__(self, start_date='01.01.2023', end_date='31.12.2023'):
        self.__start_date = self.get_format_to_date(start_date)
        self.__end_date = self.get_format_to_date(end_date)
        self.__knn = self.get_month_day(self.__start_date)
        self.__knk = self.get_month_day(self.__end_date)
        self.__m = (lambda s, e: e.month -
                    s.month)(self.__start_date, self.__end_date)
        self.__dnn = self.__knn-(self.__start_date.day-1)
        self.__dnk = self.__end_date.day

    def get_month_day(self, data: dt):
        return calendar.monthrange(data.year, data.month)[1]

    def calculation(self, item):
        item /= 12
        item_knn = item / self.__knn
        item_knk = item / self.__knk
        if self.__end_date.month == 12 and self.__end_date.day == 31:
            calc = item * self.__m + item_knn * self.__dnn
        elif self.__start_date.day == 1 and self.__start_date.month == 1:
            calc = item * self.__m + item_knk * self.__dnk
        else:
            calc = item * (self.__m - 1) + item_knn * \
                self.__dnn + item_knk * self.__dnk
        return round(calc, 2)

    def get_contribution(self):
        return self.year[self.__start_date.year]

    def get_format_to_date(self, data):
        return dt.strptime(data, '%d.%m.%y')

    def get_to_quarter(self, key, value):
        result = []
        q = len(self.quarter)
        for i in self.quarter:
            q -= 1
            if (self.quarter[i][0] < self.__start_date <= self.quarter[i][1]):
                result.append(
                    f"{key} {i}: {round(value - (self.year[self.__end_date.year][key]/len(self.quarter)) * q, 2) }")
            elif (self.quarter[i][0] <= self.__end_date < self.quarter[i][1]):
                result.append(
                    f"{key} {i}: {round(value - (self.year[self.__end_date.year][key]/len(self.quarter)) * (i-1), 2) }")
            elif self.quarter[i][1] < self.__start_date or self.__end_date < self.quarter[i][0]:
                pass
            else:
                result.append(
                    f"{key} {i}: {self.year[self.__end_date.year][key]/len(self.quarter)}")
        result.append('')
        return result
