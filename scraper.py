# scraper.py - 

import sys
from bs4 import BeautifulSoup
import time
import re
import pprint
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Scraper:
    
    def __init__(self):
        self.n_of_accounts = 0
        
    # Requests and returns html from a webpage 
    def requestWebpageSelenium(self, url):
        print('Requesting webpage...')

        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome("chromedriver.exe", chrome_options=options)
        driver.get(url)
        #time.sleep(1)
        page = driver.page_source
        driver.quit()

        return page

    def scrape(self, n_of_accounts):
        self.n_of_accounts = n_of_accounts
        print("Top " + n_of_accounts + " accounts")
        
        webpage = self.requestWebpageSelenium('http://fantasy.premierleague.com/leagues/314/standings/c')
        soup = BeautifulSoup(webpage, 'html.parser')
        
        table = soup.find('table')
        user_teams = table.find_all('a', {'class', "Link-a4a9pd-1 jwJFdW"})
        
        user_teams = user_teams[:self.n_of_accounts]
        
        team_urls = []
        regex = re.compile(r'''/entry/\d+/event/\d+''')
        for team in user_teams:
            team_url = regex.search(str(team)).group(0)
            team_url = "https://fantasy.premierleague.com/" + team_url
            print(team_url)
            team_urls.append(team_url)
            
        players_dict = {}
        for team_url in team_urls:
            print("Team: " + team_urls.index(team_url) + 1)
            webpage2 = self.requestWebpageSelenium(team_url)
            soup2 = BeautifulSoup(webpage2, 'html.parser')
            players = soup2.find_all('div', {"class": "PitchElementData__ElementName-sc-1u4y6pr-0 hZsmkV"})
            players = [player.get_text() for player in players]
            print(players)
            for player in players:
                if player not in players_dict:
                    players_dict[player] = 0
                players_dict[player] = players_dict[player] + 1
                
        return players_dict
    
    def printer(self, players):
        for key, value in sorted(players.items(), reverse=True, key=lambda item: item[1]):
            perc_in_teams = str(round((float(value)/self.n_of_accounts * 100), 2)) + "%"
            print("%s %s %s" % (key.ljust(20), perc_in_teams.rjust(8), str(value).rjust(3)))
    
    
    
print(sys.argv)
if len(sys.argv) > 1:
    n_of_accounts = int(sys.argv[1])
else:
    n_of_accounts = 10
    
scraper = Scraper()
players = scraper.scrape(n_of_accounts)
scraper.printer(players)