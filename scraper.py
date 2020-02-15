# scraper.py - 

import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Scraper:

    def __init__(self):
        self.Players = {}
        
    # Requests and returns html from a webpage 
    def requestWebpage(self, url):
        print('Requesting webpage...')

        res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36'})
        try:
            res.raise_for_status()
            res.status_code == requests.codes.ok
        except Exception as ex:
            print('There was a problem: %s' % (ex))

        return res

    def scrape(self, n_of_accounts):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome("chromedriver.exe", chrome_options=options)
        driver.get('http://fantasy.premierleague.com/leagues/314/standings/c')
        time.sleep(3)
        page = driver.page_source
        driver.quit()
        #webpage = self.requestWebpage('http://fantasy.premierleague.com/leagues/314/standings/c')
        soup = BeautifulSoup(page, 'html.parser')
        
        table = soup.find('table')
        print(table)
        
scraper = Scraper()
scraper.scrape(10)