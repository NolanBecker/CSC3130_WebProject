from selenium import webdriver
import datetime

today = str(datetime.datetime.now().date())

sites = {'Zillow': 'http://zillow.com/',
         'GameStats': 'http://na.op.gg/statistics/champion/'
         }

browser = webdriver.Chrome()

for name, link in sites.items():
    response = browser.get(link)
    html = browser.page_source

    fileName = today + '.' + name + '.html'
    outfile = open(fileName, 'w')
    outfile.write(html)
    outfile.close()

browser.quit()