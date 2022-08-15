import pandas as pd
import os
from soup import ScrapeEvent
from create_log import creating_log

logger = creating_log('cooking.py')

list_page_url = 'https://www.rivieramm.com/events'

record = dict()

header_row = ['scrappedUrl', 'eventname', 'startdate', 'enddate', 'timing', 'eventinfo', 'ticketlist',\
    'orgProfile', 'orgName', 'orgWeb', 'logo', 'sponsor', 'agendalist', 'type', 'category', 'city',\
    'country', 'venue', 'event_website', 'googlePlaceUrl', 'ContactMail', 'Speakerlist', 'online_event']

for i in header_row:
    record[i] = ''
    
try:
    with ScrapeEvent() as driver:

        links = driver.listing_page_urls(list_page_url)

        data_row = []

        for link in links:

            record = dict()
            
            if link == 'https://www.rivieramm.com/international-tug-and-salvage-convention':  # this webpage leads to a different home page
                continue


            # 1  BLOCK CODE:scraping attribute scrappedUrl 
            try:
                if driver.scrapped_url(link):
                    record['scrappedUrl'] = link
            except:
                logger.error(f'{driver.scrapped_url.__name__} Function failed', exc_info=True)
                record['scrappedUrl'] = '###'


            # 2 BLOCK CODE: scraping attribute eventtitle
            try:
                sc_title = driver.event_title()
                record['eventname'] = sc_title
            except:
                logger.error(f'{driver.event_title.__name__} Function failed', exc_info=True)
                record['eventname'] = '###'



            # 3 BLOCK CODE: scraping attribute startdate and enddate
            try:
                sc_date = driver.date()
                record['startdate'] = sc_date[0]
                record['enddate'] = sc_date[1]
            except:
                logger.error(f'{driver.date.__name__} Function failed', exc_info=True)
                record['startdate'] = '###'
                record['enddate'] = '###'


            # 5 BLOCK CODE: scraping attribute timing
            try:
                sc_timing = driver.timing()
                record['timing'] = [
                dict(type='general',
                Start_time=sc_timing['start_time'], end_time=sc_timing['end_time'],
                timezone=sc_timing['time_zone'], days='all'
                )]
            except:
                logger.error(f'{driver.timing.__name__} Function failed', exc_info=True)
                record['timing'] = '###'


            # 6 BLOCK CODE: scraping attribute eventtitle
            # try:
            #     sc_event_info = driver.event_info()
            #     record['eventinfo'] = sc_event_info
            # except:
            #     logger.error(f'{driver.event_info.__name__} Function failed', exc_info=True)
            #     record['eventinfo'] = '###'


            # 7 BLOCK CODE: scraping attribute ticketlist
            try:
                sc_ticket_list = driver.tickect_list('free')
                record['ticketlist'] = [sc_ticket_list]
            except:
                logger.error(f'{driver.tickect_list.__name__} Function failed', exc_info=True)
                record['ticketlist'] = '###'


            # 8 BLOCK CODE: scraping attribute orgProfile
            try:
                sc_org_profile = driver.org_profile()
                record['orgProfile'] = sc_org_profile
            except:
                logger.error(driver.org_profile.__name__, 'Function failed', exc_info=True)
                record['orgProfile'] = '###'


            # 9 BLOCK CODE: scraping attribute orgName
            try:
                sc_name = driver.org_name('Riviera') # Pass a string value of org_name, data can't be scraped from website nor listing page
                record['orgName'] = sc_name
            except:
                logger.error(driver.org_name.__name__, 'Function failed', exc_info=True)
                record['orgName'] = '###'


            
            # 10 BLOCK CODE: scraping attribute orgWeb
            try:
                sc_web_name = driver.org_web()
                record['orgWeb'] = sc_web_name
            except:
                logger.error(driver.org_web.__name__, 'Function failed', exc_info=True)
                record['orgWeb'] = '###'


            # 11 BLOCK CODE: scraping attribute logo
            record['logo'] = '***'


            # 12 BLOCK CODE: scraping attribute sponsor
            try:
                sc_sponsor = driver.sponsor()
                record['sponsor'] = sc_sponsor
            except:
                logger.error(driver.sponsor.__name__, 'Function failed', exc_info=True)
                record['sponsor'] = '###'


            
            # 13 BLOCK CODE: scraping attribute agendalist
            try:
                record['agendalist'] = [dict(start_time=sc_timing['start_time'],
                end_time=sc_timing['end_time'], day=f'{sc_date[0]} - {sc_date[1]}',desc='',
                title=sc_title)]
            except:
                logger.error('BLOCK 13 failed', exc_info=True)
                record['agendalist'] = '###'


            #14 BLOCK CODE: scraping attribute type
            record['type'] = '***'
            #15 BLOCK CODE: scraping attribute category
            record['category'] = '***'


            try:
                # 16 BLOCK CODE: scraping attribute city
                record['city'] = sc_timing['city']  # from block BLOCK 5

                # 17 BLOCK CODE: scraping attribute country
                record['country'] = sc_timing['country']

                # 18 BLOCK CODE: scraping attribute venue
                record['venue'] = sc_timing['venue']
            except:
                logger.error('BLOCK 16, 17, 18 failed', exc_info=True)
                record['city'] = '###'
                record['country'] = '###'
                record['venue'] = '###'


            # 19 BLOCK CODE: scraping attribute event_website
            try:
                record['event_website'] = link
            except:
                logger.error('BLOCK 19 failed', exc_info=True)
                record['event_website'] = '###'


            # 20 BLOCK CODE: scraping attribute googlePlaceUrl
            try:
                if sc_timing['country'] == 'ONLINE':
                    record['googlePlaceUrl'] = 'ONLINE'
                else:
                    a = driver.google_map_url(sc_timing['venue'], sc_timing['city'], sc_timing['country'])
                    record['googlePlaceUrl'] = a
            except:
                logger.error(driver.google_map_url.__name__,'Function failed',  exc_info=True)
                record['googlePlaceUrl'] = '###'


            # 21 BLOCK CODE: scraping attribute ContactMail
            try:
                sc_contact_mail = driver.contact_mail(link)
                record['ContactMail'] = [sc_contact_mail]
            except:
                logger.error(driver.contact_mail.__name__, 'Function failed', exc_info=True)
                record['contactMail'] = '###'


            # 22 BLOCK CODE: scraping attribute Speakerlist
            try:
                record['Speakerlist'] = '***'
            except:
                logger.error('BLOCK 22 failed', exc_info=True)
                record['Speakerlist'] = '###'


            # 23 BLOCK CODE: scraping attribute online_event
            try:
                if sc_timing['country'] == 'ONLINE':
                    record['online_event'] = 1
                else:
                    record['online_event'] =  0 
            except:  
                logger.error('BLOCK 23 failed', exc_info=True)
                record['online_event'] = '###'


            data_row.append(record)        



except Exception as err:
    logger.error('ERROR OCCURED', exc_info=True)


result_folder = 'result_tsv'

if os.path.exists(result_folder):
    for files in os.scandir(result_folder):
        os.remove(files)
else:
    os.makedirs(result_folder)

tsv_path = os.path.join(os.getcwd(), result_folder)

df = pd.DataFrame(columns=header_row, data=data_row)
df.to_csv(f'{tsv_path}/riviera.tsv', sep='\t', index=False)