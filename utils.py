
from datetime import datetime

def date_transformation(x:str) -> tuple:
    
    x = x.strip().lower()
    y = x.split('-')
    start_date = datetime.strptime(y[0].strip(), '%d %B %Y')
    end_date = datetime.strptime(y[1].strip(),  '%d %B %Y')

    return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')

from posixpath import split


def time_transformation(x:str, y:str):
    x = x.strip()
    x = x.split('-')
    start_time, end_time = x[0].strip(), x[1].strip()

    y = y.strip()
    y = y.split('-')
    time_zone = y[0].upper()

    i = int(start_time[:2])
    j = int(end_time[:2])

    if i >= 12:
        start_time = start_time + 'PM'
    else:
        start_time = start_time + 'AM'
    

    if j >= 12:
        end_time = end_time + 'PM'
    else:
        end_time = end_time + 'AM'

    return start_time, end_time, time_zone

