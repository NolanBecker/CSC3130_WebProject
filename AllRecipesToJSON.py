import requests
import datetime
import json
import re
import os
from bs4 import BeautifulSoup
from collections import OrderedDict

today = str(datetime.datetime.now().date())

response = []

urlAllRecipes = 'http://allrecipes.com/recipes/?sort=Newest'
pageAllRecipes = requests.get(urlAllRecipes)
soup = BeautifulSoup(pageAllRecipes.content, 'lxml')

for grid in soup.find_all(id="grid"):
    for position in grid.find_all("article", class_=re.compile("grid-col--fixed-tiles$")):
        if position.find("ar-save-item") is not None:
            nameTag = position.find("ar-save-item")
            name = nameTag['data-name'].replace('"', '').strip()
            description = position.find(class_="rec-card__description").string
            if description is None:
                description = "No description found."
            ratingTag = position.find("div", class_="rating-stars")
            if ratingTag is None:
                rating = "No rating found."
            else:
                rating = ratingTag['data-ratingstars']
            authorTag = position.find('h4')
            author = authorTag.contents[1].strip()

            response.append(OrderedDict([('Name', name),
                                         ('Description', description),
                                         ('Rating', rating),
                                         ('Author', author)]))
            # print(name)
            # print(description)
            # print("Rating:", rating)
            # print("Recipe by:", author)
            # print("")

if not os.path.exists('JSON/'):
    os.makedirs('JSON/')
postingsFile = 'JSON/' + today + '.AllRecipes.json'

with open(postingsFile, 'w') as outfile:
    json.dump(response, outfile, sort_keys=False, indent=2)

outfile.close()
