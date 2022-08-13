from dataclasses import dataclass
import os
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import utils


chrome_webdriver_path = os.path.join(os.getcwd(), 'chrome_webdriver', 'chromedriver')
handler = webdriver.Chrome(chrome_webdriver_path)

@dataclass
class ScrapeEvent:
    driver_handler: WebDriver = handler


    def __enter__(self):
        return self


    def __exit__(self, exc_type=None, exc_value=None, exc_tb=None):
        print('\nEXITING HEADLESS BROWSER MODE AND CLOSING ALL TABS\n')
        if  exc_type or exc_value or exc_tb is not None:
            print(f"""ERROR OCCURED:
            EXCEPTION_CLASS --- {exc_type}, 
            EXCEPTION_INSTANCE --- {exc_value}, 
            TRACEBACK --- {exc_tb}""", sep='\n')
            self.driver_handler.quit()
        else:
            self.driver_handler.quit()


    def listing_page_urls(self, url:str) -> list:
        self.driver_handler.implicitly_wait(10)
        self.driver_handler.get(url)
        x = self.driver_handler.find_elements(By.XPATH, '//h2[@class="aos-ArticleTitle aos-DS34-H2 aos-FL aos-W100 aos-M0"]/a')
        all_links = [i.get_attribute('href') for i in x]
        return all_links


    def scrapped_url(self, web_addr:str) -> bool:
        try:
            self.driver_handler.get(web_addr)
        except:
            pass
            # self.__exit__()
        else:
            return True


    def event_title(self) -> str:
        try:
            title = WebDriverWait(self.driver_handler, 5).until(
                EC.presence_of_element_located((By.ID, 'aos-EventTitle'))
            ).text
        except:
            pass
        else:
            return title


    def date(self) -> tuple:
        "extract and returns both startdate and enddate"
        try:
            sc_date = WebDriverWait(self.driver_handler, 5).until(
                EC.presence_of_element_located((By.ID, 'aos-ArticleDate'))
            ).text
        except:
            pass
        else:
            transf_date = utils.date_transformation(sc_date)
            return transf_date 
        
    def timing(self) -> dict:
        try:
            sc_time = WebDriverWait(self.driver_handler, 5).until(
                EC.presence_of_element_located((By.ID, 'aos-ArticleTime'))
            ).text
            sc_location = WebDriverWait(self.driver_handler, 5).until(
                EC.presence_of_element_located((By.ID, 'aos-ArticleLocation'))
            ).text
        except:
            pass
        else:
            transf_time = utils.time_transformation(sc_time, sc_location)
            return transf_time
    
    def event_info(self):
        "extract and returns both startdate and enddate"
        try:
            eventinfo = WebDriverWait(self.driver_handler, 5).until(
                EC.presence_of_element_located((By.TAG_NAME, 'strong'))
            ).text
        except:
            pass
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
            pass
        else:
            return x

    def org_web(self) -> str:
        try:
            # implicit wait would cover for lag
            a = self.driver_handler.find_element(By.LINK_TEXT, 'Home')
            a.click()
            a = self.driver_handler.current_url
        except:
            pass
        else:
            return a

    def sponsor(self, x:str) -> str:
        try:
            pass
        except:
            pass
        else:
            return x

    def contact_mail(self) -> str:
        try:
            a = self.driver_handler.find_element(By.PARTIAL_LINK_TEXT, '.com').text
        except:
            pass
        else:
            return a

    def google_place_url(self):
        return '***'