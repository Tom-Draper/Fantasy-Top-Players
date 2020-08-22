# Fantasy-Top-Players
A python script to retrieve and calculate the frequency of premier league players found in the teams at the top of the global fantasy league.

As the official Fantasy website uses a large amount of JavaScript, web scraping required using the Selenium web driver. This means the program takes a while to run as many webpages are fetched, especially when retriving the top 15+ teams. It seems each additional user accounts team adds an extra ~3 seconds to runtime. I aim to improve the efficiency of this implementation in future.

Currently the maximum number of accounts to include is 41. I aim to increase this in future.

-------------------------------------------------------

## Getting Started
Run scraper.py followed by the number of top accounts you wish to include (e.g. "python scraper.py 10" will return frequency of premier league players found in the current top 10 fantasy accounts globally).

Ensure that your chrome driver is the same version as your installed Chrome browser.    
The default path is "C:\Program Files\ChromeDriver\chromedriver.exe" (Windows)

### Prerequisites
Required Python modules:
- Beautiful soup (bs4)
- Regular expressions (re)
- Selenium
- Chromedriver compatible with your installed version of chrome
