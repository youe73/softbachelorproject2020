
from scraper.scraperclass import Datascraper
import time
from database import mongo
import re
import chardet


data = Datascraper()
mongo = mongo()

response = data.requesting_url("https://www.globalis.dk/Lande")
result = data.get_soup(response)
dicts = {}
link = result.find_all("a",class_="list-links__link")

count=0
for x in link:    
    if count<201:
        dicts = {"countrynames":x.text}
        #mongo.insert(dicts)
    count+=1


