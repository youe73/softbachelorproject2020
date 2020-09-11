from scraper.scraperclass import Datascraper
import time
from database import mongo
import re

class proffdata:

    def search_proff(self,url):
        data = Datascraper()
        response = data.requesting_url(url)
        soup = data.get_soup(response)
        category = data.findclasstag(soup,"three-aligned-columns clear") 
        catlist = [] 
        cattextlist = []       
        for a in category.find_all('a'):            
            catlist.append(a.get('href')) 
            cattextlist.append(a.text)                   
        return catlist, cattextlist

if __name__ == "__main__":
    attributedict = {}
    letters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","R","S","T","U","V"]
    proff = proffdata()
    datarequest = Datascraper()
    db = mongo()
    print(db)
    count = 0
    
    for l in letters:
        url ="https://www.proff.dk/industry/select?beginLetter="+l  
        categoryurl, categorytext = proff.search_proff(url) 
        for caturl in categoryurl:
            caturl = "https://www.proff.dk"+str(caturl).rstrip("\n")
            
            continues = True
            while continues == True:
                resp = datarequest.requesting_url(caturl)
                soupbase = datarequest.get_soup(resp)
                blocks = soupbase.find_all(class_="search-block-info")
                for bl in blocks:
                    name = bl.find("h3").text                    
                    name = name.strip()
                    org = bl.find("div", class_="org-number").text
                    cvr = str(org).split(" ")[-2]
                    cvrp = str(org).split(" ")[-1].strip()
                    cvr = cvr.replace("CVRP-nr","").strip()
                    
                    address = bl.find("div", class_="address").text
                    address = address.replace("Kort","")                    
                    address = address.strip()
                    brancher = bl.find("div", class_="categories ui-wide").text
                    brancher = brancher.replace("Brancher:","")
                    brancher = brancher.rstrip()
                    brancher = brancher.strip()

                    print(count)
                    attributedict = {"ID":count,"Name":name, "CVR":cvr, "CVRP":cvrp,"Address":address,"Branche":brancher}
                    print(attributedict)
                    #db.insert(attributedict)
                    count+=1
                if soupbase.find("li", class_="next"):
                    next = soupbase.find("li", class_="next")
                    searchpart = next.find('a').get('href')
                    nexturl = "https://www.proff.dk" + str(searchpart)                    
                    caturl = nexturl
                else:
                    continues=False
                    
        print("processing letter:",l)
    print("done")            
            



    