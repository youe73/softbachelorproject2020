from scraper.scraperclass import Datascraper
import re


class proffdata:

    def get_data_from_proff(self,url):
        data = Datascraper()        
        cvr = ""
        branche = ""
        startdate =""
        address= ""
        zipcode = ""
        city=""    
        employee=""
        resp = data.requesting_url(url) 
        proffinfo = data.get_soup(resp)
        if not data.findclasstag(proffinfo,"panel official-info"):
            print("Proff page has not content")
            return cvr, branche, address, zipcode, city, startdate, employee
        else:
            officiel = data.findclasstag(proffinfo,"panel official-info")                       
            li = data.findallclasstags(officiel,"clear","li")
            for a in li:        
                if "Juridisk navn" in str(a):
                    name = a.find("span").text                                      
                elif "CVR-nr" in str(a):
                    cvr = a.find("span").text  
                elif "NACE-branche" in str(a):
                    branche = a.find("span").text
                elif "Adresse" in str(a):
                    address,zipcode,city = self.address_decompose(a.find("span").text)                  
                elif "Startdato" in str(a):
                    startdate = a.find("span").text                   
                elif "Antal ansatte" in str(a):
                    employee = a.find("span").text
            return cvr, branche, address, zipcode, city, startdate, employee 

    def search_proff_by_name(self,name):    
        data = Datascraper()    
        infourlsite = ""
        cvr, branch, address, zipcode, city, startdate, employee = "","","","","","",""
        url = "https://www.proff.dk/branches%C3%B8g?q="+str(name)
        response = data.requesting_url(url) 
        result = data.get_soup(response)
        if result.find_all("div",class_="search-block-wrap"):
            for names in result.find_all("div",class_="search-block-wrap"):                
                namelinks = names.find("a").text 
                namelinks = namelinks.strip()
                name = name.strip()                              
                if name.lower() == namelinks.lower() or name.lower()+"a/s"==namelinks.lower() or name.lower()+"aps"==namelinks.lower(): 
                    infourl = names.find("a").get("href")
                    infourlsite = "https://www.proff.dk" + str(infourl)
                    cvr, branch, address, zipcode, city, startdate, employee = self.get_data_from_proff(infourlsite)
        elif result.find("div",class_="search-block-wrap"):                            
            block = result.find("div",class_="search-block-wrap")
            namelink = block.find("a").text
            namelink = namelink.strip()
            name = name.strip()
            if name.lower() == namelink.lower() or name.lower()+"a/s"==namelink.lower() or name.lower()+"aps"==namelink.lower():     
                print("One result")           
                infourl = block.find("a").get("href")
                infourlsite = "https://www.proff.dk" + str(infourl)
                cvr, branch, address, zipcode, city, startdate, employee = self.get_data_from_proff(infourlsite)
        else:
            print("There are no mathces in Proff")
            return cvr, branch, address, zipcode, city, startdate, employee, infourlsite
       
        return cvr, branch, address, zipcode, city, startdate, employee, infourlsite

    def address_decompose(self,txt):
        street, zip, city ="","",""
        match = re.search(r'\d{4}',txt)
        if match:
            pos = match.span()        
            zip = txt[pos[0]:pos[1]]
            part = txt.split(zip)
            street = part[0]
            city = part[1]
        return street, zip, city

    