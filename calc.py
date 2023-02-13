from datetime import datetime as dt, timedelta, date
import calendar
import pandas as pd


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

    @staticmethod
    def get_month_day(date):
        return calendar.monthrange(date.year, date.month)[1]

    def calculation(self, item):
        if self.__end_date.month == 12 and self.__end_date.day == 31:
            return round(((item/12)*self.__m+(item/12/self.__knn)*self.__dnn), 2)
        elif self.__start_date.day == 1 and self.__start_date.month == 1:
            return round(((item/12)*self.__m+(item/12/self.__knk)*self.__dnk), 2)
        else:
            return round(((item/12)*(self.__m-1)+(item/12/self.__knn)*self.__dnn + (item/12/self.__knk)*self.__dnk), 2)

    def get_contribution(self):
        return self.year[self.__start_date.year]

    @classmethod
    def get_format_to_date(date):
        return dt.strptime(date, '%d.%m.%y')

    def get_to_quarter(self, key, value):
        result = []
        q = len(self.quarter)
        for i in self.quarter:
            q -= 1
            # 1: [dt(2023,1,1), dt(2023,3,31)],
            # 2: [dt(2023,4,1), dt(2023,6,30)],
            # 3: [dt(2023,7,1), dt(2023,9,30)],
            # 4: [dt(2023,10,1), dt(2023,12,31)]
            # '1.12.23'
            print(value, '-', self.year[self.__end_date.year]
                  [key], '/', len(self.quarter),  '*', (i-1))
            # and self.quarter[i][0] == start_date:
            if (self.quarter[i][0] < self.__start_date <= self.quarter[i][1]):
                result.append(
                    f"{key} {i}: {round(value - (self.year[self.__end_date.year][key]/len(self.quarter)) * q, 2) }")
            # and self.quarter[i][1] == end_date:
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


start_date = '02.01.23'
end_date = '01.12.23'

cl = Calc(start_date, end_date)
tax_type = cl.get_contribution()
res = {key: cl.calculation(value) for key, value in tax_type.items()}
res1 = [cl.get_to_quarter(key, value) for key, value in res.items()]
[print(*i, sep='\n') for i in res1]
print(*res.items(), sep='\n')
print('Итог:', sum(res.values()))
