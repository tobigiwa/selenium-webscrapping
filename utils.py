
from datetime import datetime

def date_transformation(x:str) -> tuple:

    date_format = '%d %B %Y'

    if '-' in x:
        x = x.strip().lower()
        y = x.split('-')
        start_date = datetime.strptime(y[0].strip(), date_format)
        end_date = datetime.strptime(y[1].strip(),  date_format)

        return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')
    else:
        x = x.strip().lower()
        start_date = datetime.strptime(x.strip(), date_format)
        end_date = datetime.strptime(x.strip(),  date_format)

        return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')



def time_transformation(x:str, y:str) -> dict:

    # accounting for time
    x = x.strip()
    x = x.split('-')
    start_time, end_time = x[0].strip(), x[1].strip()

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

    
    # accounting for location and time zone
    y = y.strip() # removes traling spaces

    if '-' in y:  # accounting for examples like 'BST - ONLINE'
        y = y.split('-')
        time_zone, country = y[0].strip().upper(), y[1].strip().upper()

        return dict(start_time=start_time, end_time=end_time, venue='', city='', country=country, time_zone=time_zone)

    elif len(y.split()) == 1: # accounting single value e,g 'LONDON'
        y = y.upper()
        country = y
        return dict(start_time=start_time, end_time=end_time, venue='', city='', country=country, time_zone='')


    else:                   # acoounting for values like 'ABCD, DEFG' and 'AB, CD, ED' as venue, city and country
        y = y.split(',')
        if len(y) == 2:
            city, country =y[0].strip().upper(), y[1].strip().upper()
            return dict(start_time=start_time, end_time=end_time, venue='', city=city, country=country, time_zone='')

        elif len(y) == 3:
            venue, city, country = y[0].strip().upper(), y[1].strip().upper(), y[2].strip().upper()
            return dict(start_time=start_time, end_time=end_time, venue=venue, city=city, country=country, time_zone='')
        else:
            pass
