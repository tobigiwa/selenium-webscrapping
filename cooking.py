import logging
from scrape_event import ScrapeEvent
from create_log import creating_log
import os
import csv



logger = creating_log('work.py')

data_row = []

try:
    with ScrapeEvent() as driver:

        # BLOCK CODE:scraping attribute scrappedUrl 
        try:
            url = 'https://www.rivieramm.com/events/container-shipping-trade-webinar-week'
            if driver.scrappedUrl(url):
                data_row.append(url)
            else:
                pass
        except:
            logger.error('scrappedUrl Function failed')
            

        # BLOCK CODE: scraping attribute eventtitle
        try:
            sc_title = driver.event_name()
        except:
            logger.error('event_name Function failed')
        else:
            data_row.append(sc_title)

        
        # BLOCK CODE: scraping attribute startdate and enddate
        try:
            sc_date = driver.date()
            pass
        except:
            logger.error('date Function failed')
        else:
            data_row.append(sc_date[0])
            data_row.append(sc_date[1])

        
        # BLOCK CODE: scraping attribute timing
        try:
            sc_timing = driver.timing()

            dictionary = dict(type='general',
            Start_time=sc_timing[0], end_time=sc_timing[1],
            timezone=sc_timing[2], days='all'
            )
            pass
        except:
            logger.error('time Function failed')
        else:
            data_row.append(dictionary)


        # BLOCK CODE: scraping attribute eventtitle
        try:
            sc_event_info = driver.event_info()
        except:
            logger.error('event_info Function failed')
        else:
            data_row.append(sc_event_info)

            


        















except Exception as err:
    logger.exception('Exception ocurred')

else:
    result_folder = 'result_tsv'
    if os.path.exists(result_folder):
        for files in os.scandir(result_folder):
            os.remove(files)
    else:
        os.makedirs(result_folder)

    path = os.path.join(os.getcwd(), result_folder)

    header_row = ['scrappedURL', 'eventname', 'startdate', 'enddate', 'timming', 'eventinfo', 'ticketlist',\
        'orgProfile', 'orgName', 'orgWeb', 'logo', 'sponsor', 'agendalist', 'type', 'category', 'city',\
        'country', 'venue', 'event_website', 'googlePlaceUrl', 'ContactMail', 'Speakerlist', 'online_event']

    with open(f'{path}/scape_data.tsv', 'w+') as tsv_file:
            writer = csv.writer(tsv_file, delimiter='\t')
            writer.writerow(header_row)
            if len(data_row) == 23:
                writer.writerow(data_row)
            else:
                logger.info('SCRAPED RESULT INCOMPLETE, DATA NOT INCLUDED')
finally:
    print(data_row)

