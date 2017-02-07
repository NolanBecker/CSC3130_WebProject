import requests
import datetime
import json
import os
import re
from bs4 import BeautifulSoup
from collections import OrderedDict

today = str(datetime.datetime.now().date())

response = []

urlEpicurious = 'http://www.epicurious.com/search/?sort=newest&content=recipe'
pageEpicurious = requests.get(urlEpicurious)
soup = BeautifulSoup(pageEpicurious.content, 'lxml')

for section in soup.find_all('section', role='main'):
    for div in section.find_all('div', class_='results-group'):
        for article in div.find_all('article', class_='recipe-content-card'):
            data = article.find('header', class_='summary')
            name = data.find(itemprop='name').a.string
            description = data.p.string
            rating = data.find('dl', class_='recipes-ratings-summary').find('span', class_='reviews-count-container')\
                .find('dd', class_='rating').find(itemprop='ratingValue').string
            reviews= data.find('dl', class_='recipes-ratings-summary').find('span', class_='reviews-count-container')\
                .find('dd', class_='reviews-count').string

            response.append(OrderedDict([('Name', name),
                                         ('Description', description),
                                         ('Rating', rating+'/4'),
                                         ('Reviews', reviews)]))
            print(name)

path = '/home/nolan/Programming/CSC3130_WebProject/JSON/'
if not os.path.exists(path):
    os.makedirs(path)
postingsFile = path + today + '.Epicurious.json'

with open(postingsFile, 'w') as outfile:
    json.dump(response, outfile, sort_keys=False, indent=2)

outfile.close()
