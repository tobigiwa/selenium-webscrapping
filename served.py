import time

st = time.time()

from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import logging
import os
from datetime import datetime
import pandas as pd



def creating_log(script_name:str):

    log_folder_path = 'log_folder'

    if os.path.exists(log_folder_path):
        for files in os.scandir(log_folder_path):
            os.remove(files)
    else:
        os.makedirs(log_folder_path)

    log_path = os.path.join(os.getcwd(), log_folder_path, 'riviera.log')

    logger = logging.getLogger(script_name)
    logger.setLevel(logging.DEBUG)
    log_handler = logging.FileHandler(log_path)
    log_format = logging.Formatter('%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s \n')
    log_handler.setFormatter(log_format)
    logger.addHandler(log_handler)
    logger.info('Log reporting is instantiated.')

    return logger

logger = creating_log('riviera.py')

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

chrome_webdriver_path = os.path.join(os.getcwd(), 'chrome_webdriver', 'chromedriver')
handler = webdriver.Chrome(chrome_webdriver_path)

@dataclass
class ScrapeEvent:

    web_browser_driver: WebDriver = handler

    def __enter__(self):
        return self


    def __exit__(self, exc_type=None, exc_value=None, exc_tb=None):
        print('\nEXITING HEADLESS BROWSER...AWAITING SUCCESS MESSAGE\n')

        if  exc_type or exc_value or exc_tb is not None:

            print(f"""ERROR OCCURED:
            EXCEPTION_CLASS --- {exc_type}, 
            EXCEPTION_INSTANCE --- {exc_value}, 
            TRACEBACK --- {exc_tb}""", sep='\n')

            self.web_browser_driver.quit()
            print('MSG: EXIT SUCCESSFUL')
        else:
            self.web_browser_driver.quit()
            print('MSG: EXIT SUCCESSFUL')


    def listing_page_urls(self, url:str) -> list:
        try:
            self.web_browser_driver.implicitly_wait(10)
            self.web_browser_driver.get(url)
            x = self.web_browser_driver.find_elements(By.XPATH, '//h2[@class="aos-ArticleTitle aos-DS34-H2 aos-FL aos-W100 aos-M0"]/a')
            all_links = [i.get_attribute('href') for i in x]
        except:
            logger.error('listig_page_url Function failed', exc_info=True)
        return all_links


    def scrapped_url(self, web_addr:str) -> bool:
        try:
            self.web_browser_driver.get(web_addr)
        except:
            logger.error('scrapped_url Function failed', exc_info=True)
            self.__exit__()
        else:
            return True


    def event_title(self) -> str:
        try:
            title = WebDriverWait(self.web_browser_driver, 5).until(
                EC.presence_of_element_located((By.ID, 'aos-EventTitle'))
            ).text
        except:
            logger.error('event_title Function failed', exc_info=True)
        else:
            return title


    def date(self) -> tuple:
        "extract and returns both startdate and enddate"
        try:
            sc_date = WebDriverWait(self.web_browser_driver, 5).until(
                EC.presence_of_element_located((By.ID, 'aos-ArticleDate'))
            ).text
        except:
            logger.error('date Function failed', exc_info=True)
        else:
            transf_date = date_transformation(sc_date)
            return transf_date 


    def timing(self) -> dict:
        try:
            sc_time = WebDriverWait(self.web_browser_driver, 5).until(
                EC.presence_of_element_located((By.ID, 'aos-ArticleTime'))
            ).text
            sc_location = WebDriverWait(self.web_browser_driver, 5).until(
                EC.presence_of_element_located((By.ID, 'aos-ArticleLocation'))
            ).text
        except:
            logger.error('timing Function failed', exc_info=True)
        else:
            transf_time = time_transformation(sc_time, sc_location)
            return transf_time


    def event_info(self):
        "extract and returns both startdate and enddate"
        try:
            eventinfo = WebDriverWait(self.web_browser_driver, 5).until(
                EC.presence_of_element_located((By.ID, 'aos-EventMainInfo'))
            ).text
        except:
            logger.error('event_info Function failed', exc_info=True)
        else:
            return eventinfo


    def tickect_list(self, *args, **kwargs) -> dict:
        if not args or kwargs:
            return ''
        else:
            if args or kwargs == 'free':
                return dict(type='free', price='', currency='')
            else:
                pass


    def org_profile(self, x:str) -> str:
        if not x:
            return ''
        else:
            return x


    def org_name(self, x:str) -> str:
        try:
            pass
        except:
            logger.error('org_name Function failed', exc_info=True)
        else:
            return x


    def org_web(self) -> str:
        try:
            # implicit wait would cover for lag
            a = self.web_browser_driver.find_element(By.LINK_TEXT, 'Home')
            a.click()
            a = self.web_browser_driver.current_url
            self.web_browser_driver.back()
        except:
            logger.error('org_web Function failed', exc_info=True)
        else:
            return a


    def sponsor(self):
        try:

            l_sponsor = WebDriverWait(self.web_browser_driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//div[@id="aos-EventLogo"]/img'))
                )
            l_sponsor = l_sponsor.get_attribute('title')
        except:
            logger.error('sponsor Function failed', exc_info=True)
        else:
            return l_sponsor


    def google_map_url(self, *args) -> str:
        search_word = ''
        for params in args:
            search_word += str(params).strip() + ' '
        try:
            self.web_browser_driver.get('http://google.com')
            try:
                click_cookie = WebDriverWait(self.web_browser_driver, 2).until(
                    EC.presence_of_element_located((By.ID, 'L2AGLb'))
                    )
                click_cookie.click()
            except:
                pass

            search = WebDriverWait(self.web_browser_driver, 5).until(
                    EC.presence_of_element_located((By.NAME, 'q'))
                )
            search.send_keys(search_word)
            search.send_keys(Keys.RETURN)

            map_url = WebDriverWait(self.web_browser_driver,10).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, 'Maps'))
                )
            map_url.click()
            time.sleep(3)
            map_url = self.web_browser_driver.current_url
            time.sleep(1)
        except:
            logger.error('google_map_url Function failed', exc_info=True)
        else:
            return map_url


    def contact_mail(self, x) -> dict:
        try:
            self.web_browser_driver.get(x)
            contact_name = WebDriverWait(self.web_browser_driver, 5).until(
                EC.presence_of_element_located((By.ID, 'aos-ContactName'))
            ).text
            contact_email = WebDriverWait(self.web_browser_driver, 5).until(
                EC.presence_of_element_located((By.ID, 'aos-ContactEmail'))
            ).text
            a = [contact_email]
        except:
            logger.error('contact_mail Function failed', exc_info=True)
        else:
            return a


listing_page_url = 'https://www.rivieramm.com/events'

record = dict()

header_row = ['scrappedUrl', 'eventname', 'startdate', 'enddate', 'timing', 'eventinfo', 'ticketlist',\
    'orgProfile', 'orgName', 'orgWeb', 'logo', 'sponsor', 'agendalist', 'type', 'category', 'city',\
    'country', 'venue', 'event_website', 'googlePlaceUrl', 'ContactMail', 'Speakerlist', 'online_event']

for i in header_row:
    record[i] = ''
    
try:
    with ScrapeEvent() as driver:
        try:
            links = driver.listing_page_urls(listing_page_url) 
        except:
            logger.error(f'{driver.listing_page_urls.__name__} Function failed', exc_info=True)
        

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
            
            profile = 'Riviera has been providing the maritime, offshore and energy communities with quality multi-platform media services for over 20 years.'

            # 8 BLOCK CODE: scraping attribute orgProfile
            try:
                sc_org_profile = driver.org_profile(profile)
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
            record['logo'] = ''


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
            record['type'] = ''
            #15 BLOCK CODE: scraping attribute category
            record['category'] = ''


            try:
                # 16 BLOCK CODE: scraping attribute city
                record['city'] = sc_timing['city']  # from block BLOCK 5

                # 17 BLOCK CODE: scraping attribute country
                if sc_timing['country'] == 'ONLINE':
                    record['country'] = ''
                else:
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
                    record['googlePlaceUrl'] = ''
                else:
                    a = driver.google_map_url(sc_timing['venue'], sc_timing['city'], sc_timing['country'])
                    record['googlePlaceUrl'] = a
            except:
                logger.error(driver.google_map_url.__name__,'Function failed',  exc_info=True)
                record['googlePlaceUrl'] = '###'


            # 21 BLOCK CODE: scraping attribute ContactMail
            try:
                sc_contact_mail = driver.contact_mail(link)
                record['ContactMail'] = sc_contact_mail
            except:
                logger.error(driver.contact_mail.__name__, 'Function failed', exc_info=True)
                record['contactMail'] = '###'


            # 22 BLOCK CODE: scraping attribute Speakerlist
            try:
                record['Speakerlist'] = ''
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

et = time.time()

print('time elpased----', (et - st)/60)