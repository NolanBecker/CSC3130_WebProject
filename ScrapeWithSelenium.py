from selenium import webdriver
import datetime
import os

today = str(datetime.datetime.now().date())

sites = {'AllRecipes': 'http://allrecipes.com/recipes/?sort=Newest',
         'Epicurius': 'http://www.epicurious.com/search/?sort=newest&content=recipe',
         'Delish': 'http://www.delish.com/recipes/'
         }

browser = webdriver.Chrome()

for name, link in sites.items():
    response = browser.get(link)
    html = browser.page_source

    path = 'Programming/CSC3130_WebProject/HTML/Selenium/'
    if not os.path.exists(path):
        os.makedirs(path)
    fileName = path + today + '.' + name + '.html'
    outfile = open(fileName, 'w')
    outfile.write(html)
    outfile.close()

browser.quit()