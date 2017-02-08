import requests
import datetime
import json
import os
import re
from bs4 import BeautifulSoup
from collections import OrderedDict

today = str(datetime.datetime.now().date())

response = []

urlDelish = 'http://www.delish.com/recipes/'
pageDelish = requests.get(urlDelish)
soup = BeautifulSoup(pageDelish.content, 'lxml')

name = ''
description = ''
time = ''
difficulty = ''

for div in soup.find_all('div', class_='landing-feed--special-content'):
    for title in div.find_all('a', class_='landing-feed--special-title'):
        name = title.string
    for abstract in div.find_all('div', class_='landing-feed--story-abstract'):
        if abstract is not None:
            description = abstract.string[1:]
        else:
            description = "No description found"
    for meta in div.find_all('div', class_='landing-feed--recipe-meta'):
        for metaTime in meta.find_all('div', class_='recipe-info-total-time'):
            if metaTime is not None:
                time = metaTime.contents[2]
        for metaDiff in div.find_all('div', class_='recipe-info-difficulty'):
            if metaDiff is not None:
                difficulty = metaDiff.contents[2]

    response.append(OrderedDict([('Name', name),
                                 ('Description', description),
                                 ('Time', time),
                                 ('Difficulty', difficulty)]))

cwd = os.path.dirname(os.path.realpath(__file__)) + "/"
path = 'JSON/'
if not os.path.exists(path):
    os.makedirs(path)
postingsFile = cwd + path + today + '.Delish.json'

with open(postingsFile, 'w') as outfile:
    json.dump(response, outfile, sort_keys=False, indent=2)

outfile.close()
