import numpy as np
import datetime as dt

class pto:
    # the purpose of this class is to identify the longest possible break one could achieve
    # based on the amount of days they want to take off. 
    # This will output the best selection of dates to maximise the length of a vacation.
    # If there are mutliple instances / combinations that amount to the same vacation time,
    # The one that is soonest will be shown
    
    def __init__(self, pto_days, constants, start=None, end=None, holidays = None):
        self.pto_days = pto_days
        self.constants = constants
        if type(start) == str:
            year = int(start[0:4])
            mon = int(start[5:7])
            day = int(start[8:10])
            start = dt.date(year,mon,day)

            year = int(end[0:4])
            mon = int(end[5:7])
            day = int(end[8:10])
            end = dt.date(year,mon,day)

        if start == None:
            start = dt.date.today()
            end = start + dt.timedelta(366)
        
        if holidays == None:
            holidays = self._getFedHolidays()
            
        self.start = start
        self.end = end
        self.holidays = holidays
        
        
        if type(self.holidays) == list:
            self.holidays = np.array(self.holidays).astype('datetime64').astype(dt.date)
            
        self.calendar = self._getFullYear(self.start,self.end)
        self.dayofweek = self._getDayOfWeek()
        self.month = self._getMonth()
        
        self.fed_holidays = self.fix_holidays(self.holidays)
        self.weekends = self._getWeekends(self.start,self.end)
        self.allDaysOff = self.combineDaysOff(self.fed_holidays, self.weekends)
        self.quantifiedDays = self.quantifyDays(self.calendar, self.allDaysOff)
        
        self.longestVacation = self.longestVacation(self.pto_days,self.calendar, self.quantifiedDays)
        self.suffix = self._getSuffix()
        
    def ShowSuggestions(self):
        vacation_days = self.longestVacation
        all_days_off = self.allDaysOff
        
        current_pto_days = []
        for day in vacation_days:
            if day in all_days_off:
                continue
            current_pto_days.append(day)

        print('Based on the current days off, and the amount of PTO usable, it is advisable',
               'to take the following days off to maximize your vacation:')
        if len(current_pto_days) == 0:
            print('Get a job that provides PTO, or accrue some more time')
        
        for date in current_pto_days:
            month = self.month[date.month]
            day = date.day
            weekday = self.dayofweek[date.weekday()]
            if day > 3:
                suffix = 'th'
            else:
                suffix = self.suffix[day]
            print(f'The {day}{suffix} of {month}, which falls on a {weekday}')
    
    def fix_holidays(self,holidays):
        # fixes the holidays based on how it is done in the government:
        # If it falls on Saturday, it is observed on Friday. 
        # If it falls on Sunday, it is observed on Monday
        for i,date in enumerate(holidays):
            if date.weekday() == 6: 
                holidays[i] = holidays[i] + dt.timedelta(1)
            if date.weekday() == 5:
                holidays[i] = holidays[i] - dt.timedelta(1)
                
        return holidays
    
    def combineDaysOff(self,fed_holidays,weekends):
        return np.sort(np.concatenate([weekends, fed_holidays]))
    
    def quantifyDays(self,calendar,days_off):
        out = []
        for day in calendar:
            if day in days_off:
                out.append(0)
                continue
            out.append(1)
        return np.array(out)
    
    def longestVacation(self,pto_days, calendar, quantified_arr):
        # A sliding window is used to quickly select the best dates to use PTO.
        if pto_days >= len(calendar):
            print('The amount of PTO days specified exceeds the timeframe considered.')
            print('Consider changing the start and end times, or reducing the number of PTO days')
            print('The number of PTO days will be reduced to the number of calendar days considered')
        d_final = 0
        while np.sum(quantified_arr[0:d_final]) <= pto_days:
            if (d_final + 1) >= len(quantified_arr): break            
            d_final += 1
            
        current_index = 0
        for i,val in enumerate(quantified_arr):
            # Check to make sure the while loop doesn't end in error
            if (d_final + i + 1) >= len(quantified_arr): break

            while np.sum(quantified_arr[i:(d_final+i+1)]) <= pto_days:
                current_index = i
                d_final +=1

        start_of_break = current_index
        end_of_break = start_of_break + d_final
        return calendar[start_of_break:end_of_break]
    
    def _getFullYear(self,start,end):
        calendar = []
        while start <= end:
            calendar.append(start)
            start += dt.timedelta(1)
        return np.array(calendar) 
    
    
    # Methods below are used to return constants.

    def _getWeekends(self,start,end):
        weekends = []
        while start <= end:
            weekday = start.weekday()
            if weekday >= 5:
                weekends.append(start)
            start = start + dt.timedelta(1)
        return np.array(weekends)
        
    def _getFedHolidays(self):
        return self.constants.FED_HOLIDAY
    
    def _getDayOfWeek(self):
        return self.constants.DAYOFWEEK
    
    def _getMonth(self):
        return self.constants.MONTH
    
    def _getSuffix(self):
        return self.constants.SUFFIX

