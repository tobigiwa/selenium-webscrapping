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


    def __exit__(self, exc_type, exc_value, exc_tb):
        print('\nEXITING HEADLESS BROWSER MODE AND CLOSING ALL TABS\n')
        if  exc_type or exc_value or exc_tb is not None:
            print(f"""ERROR OCCURED:
            EXCEPTION_CLASS --- {exc_type}, 
            EXCEPTION_INSTANCE --- {exc_value}, 
            TRACEBACK --- {exc_tb}""", sep='\n')
            self.driver_handler.quit()
        else:
            self.driver_handler.quit()


    def scrappedUrl(self, web_addr:str) -> bool:
        try:
            self.driver_handler.implicitly_wait(15)
            self.driver_handler.get(web_addr)
        except:
            pass
        else:
            return True

    def event_name(self) -> str:
        try:
            title = WebDriverWait(self.driver_handler, 10).until(
                EC.presence_of_element_located((By.ID, 'aos-EventTitle'))
            ).text
        except:
            pass
        else:
            return title

    def date(self) -> tuple:
        "extract and returns both startdate and enddate"
        try:
            sc_date = WebDriverWait(self.driver_handler, 10).until(
                EC.presence_of_element_located((By.ID, 'aos-ArticleDate'))
            ).text
        except:
            pass
        else:
            transf_date = utils.date_transformation(sc_date)
            return transf_date 
        
    def timing(self) -> tuple:
        try:
            sc_time = WebDriverWait(self.driver_handler, 10).until(
                EC.presence_of_element_located((By.ID, 'aos-ArticleTime'))
            ).text
            sc_location = WebDriverWait(self.driver_handler, 10).until(
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
            eventinfo = WebDriverWait(self.driver_handler, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'strong'))
            ).text
        except:
            pass
        else:
            return eventinfo
