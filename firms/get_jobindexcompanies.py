from scraper.scraperclass import Datascraper
import time
from database import mongo
import re

class jobindexcompanies:
    
    def firmlinks(self,url):
        listlinks = []
        data = Datascraper()
        response = data.requesting_url(url)
        soup = data.get_soup(response)
        firmslinklist = soup.find_all(class_="jix_company_name_link d-flex align-items-md-center flex-column flex-md-row")
        for links in firmslinklist:           
            listlinks.append(links.find("a",class_="text-decoration-none").get("href"))
        return listlinks

    def get_firmdetails(self,url):
        data = Datascraper()
        name = ""
        cvr = ""
        startdate =""
        address= ""
        zipcode = ""
        city=""    
        employee=""
        branch = ""
        proffarray = []
        response = data.requesting_url(url)
        soup = data.get_soup(response)        
        for links in soup.find_all("a"):           
            if "proff" in links.get("href"):                
                profflink = links.get('href')
                proffarray.append(profflink)
        if len(proffarray) == 0:
            print("No proff")
            return name, cvr, address, zipcode, city, startdate, employee, branch
        else:            
            #print(proffarray[0])
            proffres = data.requesting_url(proffarray[0])
            if proffres.status_code != 200:
                print("404 - Page does not exist")
                return name, cvr, address, zipcode, city, startdate, employee, branch
            else:
                soupproff = data.get_soup(proffres)
                officiel = soupproff.find(class_="panel official-info")
                li = officiel.find_all('li',class_="clear")                
                for a in li:        
                    if "Juridisk navn" in str(a):
                        name = a.find("span").text                                      
                    elif "CVR-nr" in str(a):
                        cvr = a.find("span").text                     
                    elif "Adresse" in str(a):
                        address,zipcode,city = data.address_decompose(a.find("span").text,",")                  
                    elif "Startdato" in str(a):
                        startdate = a.find("span").text                   
                    elif "Antal ansatte" in str(a):
                        employee = a.find("span").text
                    elif "NACE-branche:" in str(a):
                        branch = a.find("span").text
                return name, cvr, address, zipcode, city, startdate, employee, branch
        

if __name__ == "__main__":

    jobindex = jobindexcompanies()
    datarequest = Datascraper()
    db = mongo() #jobindexfirms
    print("Rows in Database ",db.count_doc())

    attributedict = {}
    url = "https://www.jobindex.dk/virksomhedsoversigt/resultat?page="
    
    count = 1
    page = 1
    continues = True
    while continues == True:
        linksurl = url + str(page) 
        resp = datarequest.requesting_url(linksurl)
        basesoup = datarequest.get_soup(resp)        
        for u in jobindex.firmlinks(linksurl):
            firmurl = "https://www.jobindex.dk" + str(u)
            name, cvr, address, zipcode, city, startdate, employee, branch = jobindex.get_firmdetails(firmurl)
            attributedict = {"ID":count, "Name": name, "CVR": cvr, "Address":address, "Zipcode": zipcode, "City":city,
            "Startdate":startdate,"Employee":employee, "Branch": branch}
            #db.insert(attributedict)
            print(count)
            count+=1
        page +=1
        if not basesoup.find("li", class_="page-item page-item-next"):
            continues= False                   
    
    print("done")
           

    