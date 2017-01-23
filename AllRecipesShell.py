import requests
import re
from bs4 import BeautifulSoup

urlAllRecipes = 'http://allrecipes.com/recipes/?sort=Newest'
pageAllRecipes = requests.get(urlAllRecipes)
soup = BeautifulSoup(pageAllRecipes.content, 'lxml')

for grid in soup.find_all(id="grid"):
    for position in grid.find_all("article", class_=re.compile("grid-col--fixed-tiles$")):
        name = position.find("ar-save-item")
        description = position.find(class_="rec-card__description")
        rating = position.find("div", class_="rating-stars")

        #print(position.prettify())
        print(name)
        print(description)
        print(rating)
        print("")
