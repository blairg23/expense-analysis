from expensive.utils import get_date
import datetime

import random

iterations = 100

start_year = 1900
end_year = 2020

datetime_count = 0
str_count = 0

for iteration in range(iterations):
    random_year = str(random.randint(start_year, end_year))
    random_month = str(random.randint(1, 12)).zfill(2)
    random_day = str(random.randint(1, 28)).zfill(2)
    random_date = '-'.join([random_year, random_month, random_day])
    date_format = '%Y-%m-%d'
    formatted_date = get_date(random_date, date_format)

    print('year:', random_year)
    print('month:', random_month)
    print('day:', random_day)
    print('date:', random_date)
    print(f'get_date({random_date}, {date_format}): {formatted_date}')
    print(f'date type: {type(formatted_date)}')
    print('-------------\n')


    if isinstance(formatted_date, datetime.date):
        datetime_count += 1
    elif isinstance(formatted_date, str):
        str_count += 1

print('Datetimes: ', datetime_count)
print('Strings: ', str_count)
