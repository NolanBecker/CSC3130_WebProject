import requests
import re
from bs4 import BeautifulSoup

urlAllRecipes = 'http://allrecipes.com/recipes/?sort=Newest'
pageAllRecipes = requests.get(urlAllRecipes)
soup = BeautifulSoup(pageAllRecipes.content, 'lxml')

for grid in soup.find_all(id="grid"):
    for position in grid.find_all("article", class_=re.compile("grid-col--fixed-tiles$")):
        if position.find("ar-save-item") is not None:
            nameTag = position.find("ar-save-item")
            name = nameTag['data-name']
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

            print(name)
            print(description)
            print("Rating:", rating)
            print("Recipe by:", author)
            print("")
