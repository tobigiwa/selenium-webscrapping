from dataclasses import dataclass
import os
import time
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import utils
from create_log import creating_log

logger = creating_log('soup.py')

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
            transf_date = utils.date_transformation(sc_date)
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
            transf_time = utils.time_transformation(sc_time, sc_location)
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
            return '***'
        else:
            if args or kwargs == 'free':
                return dict(type='free', price='***', currency='***')
            else:
                pass


    def org_profile(self, *args, **kwargs) -> str:
        if not args or kwargs:
            return '***'
        else:
            pass


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
            map_url = map_url.click()
            time.sleep(4)
            map_url = self.web_browser_driver.current_urls
            time.sleep(1.5)
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
            a = dict(name=contact_name, email=contact_email)
        except:
            logger.error('contact_mail Function failed', exc_info=True)
        else:
            return a
