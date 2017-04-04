import requests
import datetime
import json
import re
import os
from bs4 import BeautifulSoup
from collections import OrderedDict

today = str(datetime.datetime.now().date())

response = []

urlAllRecipes = 'http://allrecipes.com'
pageAllRecipes = requests.get(urlAllRecipes + '/recipes/?sort=Newest')
soup = BeautifulSoup(pageAllRecipes.content, 'lxml')

name = "No name found"
description = "No description found"

for grid in soup.find_all(id="grid"):
    for position in grid.find_all("article", class_=re.compile("grid-col--fixed-tiles$")):
        if position.find("ar-save-item") is not None:
            # nameTag = position.find("ar-save-item")
            # name = nameTag['data-name'].replace('"', '').strip()
            # description = position.find(class_="rec-card__description").string
            # if description is None:
            #     description = "No description found."
            ratingTag = position.find("div", class_="rating-stars")
            if ratingTag is None:
                rating = "No rating found."
            else:
                rating = ratingTag['data-ratingstars']
            authorTag = position.find('h4')
            author = authorTag.contents[1].strip()
            link = "No link"
            if position.find("a") is not None:
                link = urlAllRecipes + position.find("a").get("href")

            servings = "No serving size"
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

            response.append(OrderedDict([('Name', name),
                                         ('Description', description),
                                         ('Rating', rating),
                                         ('Author', author),
                                         ('Serving size', servings),
                                         ('Link', link)]))
            # print(name)
            # print(description)
            # print("Rating:", rating)
            # print("Recipe by:", author)
            # print("")

cwd = os.path.dirname(os.path.realpath(__file__)) + "/"
path = 'JSON/'
if not os.path.exists(path):
    os.makedirs(path)
postingsFile = cwd + path + today + '.AllRecipes.json'

with open(postingsFile, 'w') as outfile:
    json.dump(response, outfile, sort_keys=False, indent=2)

outfile.close()
