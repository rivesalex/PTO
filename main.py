import numpy as np
import datetime as dt
import Modules.constants as constants
import Modules.pto as pto


pto_days = int(input('Please specify the amount of days off you have: '))
start_date = input('Please specify the start date, using YYYY-MM-DD format: ')
while (len(start_date) != 10) or (start_date[4] != '-') or (start_date[7] != '-'):
    if start_date == '':
        break
    print('\nIncorrect input for the start date')
    start_date = input('Please input using YYYY-MM-DD format (include the dashes): ')

if start_date != '':
    end_date = input('Please specify the end date, using YYYY-MM-DD format: ')
    logic_check = np.datetime64(end_date) <= np.datetime64(start_date)
    while (len(end_date) != 10) or (end_date[4] != '-') or (end_date[7] != '-') or logic_check:
        if logic_check == True:
            print('\nThe end date should be after the start date')
        if logic_check == False:
            print('\nIncorrect input for the end date\n')
        end_date = input('Please input using YYYY-MM-DD format (include the dashes) and it should be later than start: ')
        logic_check = np.datetime64(end_date) <= np.datetime64(start_date)
        continue

if start_date == '':
    start_date = None
    end_date = None
print('\n')
a = pto.pto(pto_days, constants, start = start_date, end=end_date)
a.ShowSuggestions()