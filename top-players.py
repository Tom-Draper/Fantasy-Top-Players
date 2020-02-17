# top-players.py - scrapes the urls of the top n number of fantasy accounts.
# Retrieves and scrapes the names of each player in those teams.
# Cacluates and outputs over frequency of players.

import sys
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd

class Scraper:
    
    def __init__(self):
        self.n = 0
        
    def requestWebpageSelenium(self, url):
        """Requests and returns html from a webpage"""
        print('Requesting webpage...')

        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(chrome_options=options)
        driver.get(url)
        page = driver.page_source
        driver.quit()

        return page

    def scrape(self, n):
        """Scrapes and counts the players used in the top n fantasy accounts and
        returns the frequency of each player"""
        self.n = n
        print("Top " + str(n) + " accounts")
        
        users_webpage = self.requestWebpageSelenium('http://fantasy.premierleague.com/leagues/314/standings/c')
        users_soup = BeautifulSoup(users_webpage, 'html.parser')
        
        table = users_soup.find('table') # Get table of top accounts
        user_teams = table.find_all('a', {'class', "Link-a4a9pd-1 jwJFdW"})
        user_teams = user_teams[:self.n]
        
        team_urls = []
        regex = re.compile(r'''/entry/\d+/event/\d+''')
        for team in user_teams:
            team_url = regex.search(str(team)).group(0)
            team_url = "https://fantasy.premierleague.com/" + team_url
            print(team_url)
            team_urls.append(team_url)
            
        players_df = pd.DataFrame(columns=["Score", "Frequency"])
        players_df.index.name = "Players"
        
        for team_url in team_urls:
            team_rank = team_urls.index(team_url) + 1
            print("Team: " + str(team_rank))
            
            team_webpage = self.requestWebpageSelenium(team_url)
            team_soup = BeautifulSoup(team_webpage, 'html.parser')
            
            players = team_soup.find_all('div', {"class": "PitchElementData__ElementName-sc-1u4y6pr-0 hZsmkV"})
            players = [player.get_text() for player in players]
            
            print(players)
            for player in players:
                if player not in players_df.index:
                    players_df.loc[player] = [0, 0]  # Create new player row
                # Update 'relative score' (based on number of teams included) 
                # using league position of the team player was found in. 
                # Higher score = better
                players_df.at[player, 'Score'] += (len(team_urls) - (team_rank - 1))
                players_df.at[player, 'Frequency'] += 1  # Increment count
                
        
        return players_df.sort_values('Score', ascending=False)
    
    
if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    else:
        n = 35
        
    scraper = Scraper()
    players = scraper.scrape(n)
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(players)