import requests
import datetime

today = str(datetime.datetime.now()).split(' ')[0]

sites = {'Allrecipes': 'http://allrecipes.com/recipes/?sort=Newest'}

for name, link in sites.items():
    response = requests.get(link)
    html = response.content

    fileName = today + '.' + name + '.html'
    outfile = open(fileName, "wb")
    outfile.write(html)
    outfile.close()