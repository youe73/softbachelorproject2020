from scraper.scraperclass import Datascraper
import time
from database import mongo
import re
import chardet


data = Datascraper()
mongo = mongo()

response = data.requesting_url("https://edemann.dk/liste-danske-byer/")
result = data.get_soup(response)
dicts = {}
table = result.find("table")
tr = table.find_all("tr")
print(type(tr))
for x in tr:
    dicts = {"citynames":x.find("td").text}
    #mongo.insert(dicts)
    print(x.find("td").text)