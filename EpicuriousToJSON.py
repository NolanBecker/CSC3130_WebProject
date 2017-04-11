import requests
import datetime
import json
import os
import re
from bs4 import BeautifulSoup
from collections import OrderedDict

today = str(datetime.datetime.now().date())

response = []

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


            response.append(OrderedDict([('Name', name),
                                         ('Description', description),
                                         ('Author', author),
                                         ('Rating', rating),
                                         ('Reviews', reviews),
                                         ('Serves', serves),
                                         ('Link', link)]))

cwd = os.path.dirname(os.path.realpath(__file__)) + "/"
path = 'JSON/'
if not os.path.exists(path):
    os.makedirs(path)
postingsFile = cwd + path + today + '.Epicurious.json'

with open(postingsFile, 'w') as outfile:
    json.dump(response, outfile, sort_keys=False, indent=2)

outfile.close()
