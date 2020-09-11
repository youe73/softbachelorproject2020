import schedule 
import time 
from scraper.scraperclass import Datascraper
import time
import sys

incomingurl = sys.argv[1]
searching = sys.argv[2]

url = incomingurl
newurl =url + searching

crw = Datascraper()

f = open("example_newlinks.txt","a",encoding="utf-8")
newlinks = []
days = newurl.split('=')[-1]
linkpage = crw.requesting_url(newurl)
result = crw.get_soup(linkpage)
maxpages = result.find_all(class_="page-link")                    
if not maxpages:
    maxpage=1
else:
    maxpage = maxpages[-1].getText()
    print("maxpage ",maxpage)     
    count = 0
    for trip in range(int(maxpage)):
        trip+=1
        scr_url = url + "jobsoegning?page=" + str(trip) + "&jobage=14"
        print(scr_url)
        resp = crw.requesting_url(scr_url)             
        soup = crw.get_soup(resp)
        links = ""
        category = ""                        
        if soup.find_all(class_="PaidJob"):
            category = soup.find_all(class_="PaidJob") 
            for txts in category:                    
                web = txts.find_all('a', href=True)
                site = web[1].get('href')
                newlinks.append(site)    
                f.write(str(site) + "\n")                
                count+=1             
        else:
            category = soup.find_all(class_="jobsearch-result") 
            for txts in category:                    
                web = txts.find_all('a', href=True)
                site = web[0].get('href')
                newlinks.append(site)  
                f.write(str(site) + "\n")                  
                count+=1 
    print("Newest link extracted")

crw.scrape_contentfromlink(newlinks,"jobindex.dk")


