from scraper.scraperclass import Datascraper
import time
from database import mongo
import re
import chardet


data = Datascraper()
mongo = mongo()

response = data.requesting_url("https://ufm.dk/uddannelse/videregaende-uddannelse/fleksible-uddannelser/bachelorloeftet/liste-over-virksomheder")
result = data.get_soup(response)
dicts = {}
div = result.find("div",class_="documentContent")
li = div.find_all("li")
print(type(li))
for x in li:
    dicts = {"names":x.text}
    #mongo.insert(dicts)
    print(x.text)