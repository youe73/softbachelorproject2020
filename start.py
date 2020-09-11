import schedule 
import logging
import time 
from database import mongo
from scraper.scraperclass import Datascraper
from jobindex import Jobindex
import sys

incomingurl = sys.argv[1]
search = sys.argv[2]

url = incomingurl
searchword = search
data = Datascraper()
jbindex = Jobindex()

# In the terminal write start.py and the scraper starts retrieving all the links from jobindex.
# links craping will take approx. 1 hour or so.
# subsequently the job ad contents will be scraped, and the related sources such as firm info will also be searched  
rootlinks = jbindex.get_root_links(url)
topiclinks = jbindex.getall_topic_links(rootlinks,url)
area = jbindex.get_all_area(topiclinks)
topic = jbindex.make_topic_area_page(area,url)
all = jbindex.get_all_links(topic,"?page=")
newlink = data.remove_duplicate_links(all)
jbindex.scrape_contentfromlink(newlink,searchword)


"""
# an example reading from a text file with all the job links extracted
all_link = []
f = open("data_0309_2020.txt", "r", encoding="utf-8")
content = f.readlines()
count = 0
for a in content:        
    a = a.replace("(","")
    a = a.replace("'","")
    a = a.replace(")","")     
    alist = a.split(",") 
    
    #print(alist[0])
    #print(count)
    all_link.append(alist)
count+=1

print(len(all_link))
jbindex.scrape_contentfromlink(all_link,"jobindex.dk")
"""


