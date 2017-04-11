import requests
import datetime
import json
import re
import os
from bs4 import BeautifulSoup
from collections import OrderedDict

today = str(datetime.datetime.now().date())

sites = OrderedDict([])

urlAllRecipes = 'http://allrecipes.com'
pageAllRecipes = requests.get(urlAllRecipes + '/recipes/?sort=Newest')
soup = BeautifulSoup(pageAllRecipes.content, 'lxml')

name = "No name found"
description = "No description found"
rating = "No rating found"
author = "No author found"

allRecipes = []

for grid in soup.find_all(id="grid"):
    for position in grid.find_all("article", class_=re.compile("grid-col--fixed-tiles$")):
        if position.find("ar-save-item") is not None:
            link = "No link"
            if position.find("a") is not None:
                link = urlAllRecipes + position.find("a").get("href")

            if link is not "No link":
                newSoup = BeautifulSoup(requests.get(link).content, 'lxml')
                # for serv in newSoup.find_all("span", class_="servings-count"):
                #     print(serv)
                for h1 in newSoup.find_all("h1", itemprop="name"):
                    if h1.text is not None:
                        name = h1.text
                for div in newSoup.find_all("div", itemprop="description"):
                    if div.text is not None:
                        description = div.text.replace("\r\n", "").strip()[1:][:-1]
                for div in newSoup.find_all("div", class_="rating-stars"):
                    if div is not None:
                        rating = div['data-ratingstars']
                for span in newSoup.find_all("span", itemprop="author"):
                    if span.text is not None:
                        author = span.text

            allRecipes.append(OrderedDict([('Name', name),
                                         ('Description', description),
                                         ('Author', author),
                                         ('Rating', rating),
                                         ('Link', link)]))

urlDelish = 'http://www.delish.com'
pageDelish = requests.get(urlDelish + '/recipes/')
soup = BeautifulSoup(pageDelish.content, 'lxml')

name = ''
description = ''
time = ''
difficulty = ''
serves = ''
link = ''

delish = []

for div in soup.find_all('div', class_='landing-feed--special-content'):
    for title in div.find_all('a', class_='landing-feed--special-title'):
        if title.get('href') is not None:
            link = urlDelish + title.get('href')
            newSoup = BeautifulSoup(requests.get(link).content, 'lxml')
            for h1 in newSoup.find_all('h1', itemprop='name'):
                if h1.text is not None:
                    name = h1.text
            for div in newSoup.find_all('div', class_='recipe-page--body-content'):
                p = div.find('p')
                if p.text is not None:
                    description = p.text
            for timeTag in newSoup.find_all('time', itemprop='totalTime'):
                if timeTag.text is not None:
                    time = timeTag.text
            for div in newSoup.find_all('div', class_='recipe-info-difficulty'):
                if div.text is not None:
                    difficulty = div.text.replace("\nLevel: \n", "").strip()
            for div in newSoup.find_all('div', itemprop='recipeYield'):
                if div.text is not None:
                    serves = div.text
                    serves = serves.replace("\nServes: \n", "").strip()
                    serves = serves.replace("Yield: \n", "").strip()

            delish.append(OrderedDict([('Name', name),
                                         ('Description', description),
                                         ('Time', time),
                                         ('Difficulty', difficulty),
                                         ('Serves', serves),
                                         ('Link', link)]))

urlEpicurious = 'http://www.epicurious.com'
pageEpicurious = requests.get(urlEpicurious + '/search/?sort=newest&content=recipe')
soup = BeautifulSoup(pageEpicurious.content, 'lxml')

name =  ""
description = ""
author = ""
rating = ""
reviews = ""
serves = ""
link = ""

epicurioius = []

for section in soup.find_all('section', role='main'):
    for div in section.find_all('div', class_='results-group'):
        for article in div.find_all('article', class_='recipe-content-card'):
            for a in article.find_all('a', class_='view-complete-item'):
                if a is not None:
                    link = urlEpicurious + a.get('href')
                    newSoup = BeautifulSoup(requests.get(link).content, 'lxml')
                    for h1 in newSoup.find_all('h1', itemprop='name'):
                        if h1 is not None:
                            name = h1.text
                    for div in newSoup.find_all('div', itemprop='description'):
                        if div.find('p') is not None:
                            description = div.find('p').text
                    for a in newSoup.find_all('a', itemprop='author'):
                        if a is not None:
                            author = a.text
                    for span in newSoup.find_all('span', class_='rating'):
                        if span is not None:
                            rating = span.text
                    for span in newSoup.find_all('span', itemprop='reviewCount'):
                        if span is not None:
                            reviews = span.text
                    for dd in newSoup.find_all('dd', itemprop='recipeYield'):
                        if dd is not None:
                            serves = dd.text
                            serves = serves.replace(" servings", "").strip()
                            serves = serves.replace(" Servngs", "").strip()


            epicurioius.append(OrderedDict([('Name', name),
                                         ('Description', description),
                                         ('Author', author),
                                         ('Rating', rating),
                                         ('Reviews', reviews),
                                         ('Serves', serves),
                                         ('Link', link)]))


sites.update([('AllRecipes', allRecipes), ('Delish', delish), ('Epicurious', epicurioius)])
cwd = os.path.dirname(os.path.realpath(__file__)) + "/"
path = 'JSON/'
if not os.path.exists(path):
    os.makedirs(path)
postingsFile = cwd + path + today + '.json'

with open(postingsFile, 'w') as outfile:
    json.dump(sites, outfile, sort_keys=False, indent=2)

outfile.close()
