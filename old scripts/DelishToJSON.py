import requests
import datetime
import json
import os
import re
from bs4 import BeautifulSoup
from collections import OrderedDict

today = str(datetime.datetime.now().date())

response = []

urlDelish = 'http://www.delish.com'
pageDelish = requests.get(urlDelish + '/recipes/')
soup = BeautifulSoup(pageDelish.content, 'lxml')

name = ''
description = ''
time = ''
difficulty = ''
serves = ''
link = ''

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
    #     name = title.string
    #     link = urlDelish + title.get('href')
    # for abstract in div.find_all('div', class_='landing-feed--story-abstract'):
    #     if abstract is not None:
    #         description = abstract.string[1:]
    #     else:
    #         description = "No description found"
    # for meta in div.find_all('div', class_='landing-feed--recipe-meta'):
    #     for metaTime in meta.find_all('div', class_='recipe-info-total-time'):
    #         if metaTime is not None:
    #             time = metaTime.contents[2]
    #     for metaDiff in div.find_all('div', class_='recipe-info-difficulty'):
    #         if metaDiff is not None:
    #             difficulty = metaDiff.contents[2]

    response.append(OrderedDict([('Name', name),
                                 ('Description', description),
                                 ('Time', time),
                                 ('Difficulty', difficulty),
                                 ('Serves', serves),
                                 ('Link', link)]))

cwd = os.path.dirname(os.path.realpath(__file__)) + "/"
path = 'JSON/'
if not os.path.exists(path):
    os.makedirs(path)
postingsFile = cwd + path + today + '.Delish.json'

with open(postingsFile, 'w') as outfile:
    json.dump(response, outfile, sort_keys=False, indent=2)

outfile.close()
