from scraper.scraperclass import Datascraper
import time
#from database import mongo
#from db2 import db2database
import re
import chardet
from proff import proffdata
#import ibm_db
#import ibm_db_dbi

class Jobindex(Datascraper):    
    
    def get_root_links(self, url):        
        geturl = url + "job/"     
        response = self.requesting_url(url) 
        result = self.get_soup(response)        
        category = self.findallclasstags(result,"category")         
        categorylist = []               
        category = list(dict.fromkeys(category))
        for a in category:
            newurl = url[:-1] + a.get('href')            
            categorylist.append(newurl) 
        #logger.debug(categorylist)
        return categorylist

    def getall_topic_links(self,all_links, url):
        subcategorylist = []
        for links in all_links:
            response = self.requesting_url(links) 
            result = self.get_soup(response) 
            subcategory = self.findallclasstags(result,"category") 
            for a in subcategory:
                newurl = url[:-1] + a.get('href')
                subcategorylist.append(newurl)
        #logger.debug(subcategorylist) 
        return subcategorylist
        
    def get_all_area(self,all_sublinks):    
        arealist = []
        for area in all_sublinks:
            response = self.requesting_url(area) 
            result = self.get_soup(response)             
            subarea = self.findallclasstags(result,"category")        
            subarea = list(dict.fromkeys(subarea))
            for a in subarea:
                print(a.get('href'))
                arealist.append(a.get('href'))         
        #logger.debug(arealist)          
        return arealist

    def make_topic_area_page(self,areas, url):
        pagelist = []        
        for area in areas:        
            targeturl = url[:-1] + area
            pagelist.append(targeturl) 
        #logger.debug("Topics extracted")
        return pagelist

    def get_all_links(self,links,pages:str): 
        f = open("example.txt","a",encoding="utf-8")    
        all_linkpage=[] 
        extracted = ""
        for url in links:                
            rooturl = url.rstrip("\n\r") + pages  
            response = self.requesting_url(rooturl)
            result = self.get_soup(response)             
            maxpages = self.findallclasstags(result,"page-link")                        
            if not maxpages:
                maxpage=1
            else:
                maxpage = maxpages[-1].getText()
            print("maxpage ",maxpage)                                
            for trip in range(int(maxpage)):
                trip+=1
                scr_url = rooturl + str(trip)  
                print(scr_url)              
                resp = self.requesting_url(scr_url)                              
                soup = self.get_soup(resp) 
                if self.findallclasstags(soup,"PaidJob"):
                    category = self.findallclasstags(soup,"PaidJob")
                    for txts in category:
                        hreflink = txts.find_all('a', href=True)
                        title = hreflink[1].text                     
                        jobsite = hreflink[1].get('href')
                        name = hreflink[2].text 
                        dates = txts.find("time").get("datetime")                         
                        extracted = jobsite, name, title, dates   
                        if extracted not in all_linkpage:
                            all_linkpage.append(extracted) 
                            f.write(str(extracted)+"\n")                           
                else:
                    category = self.findallclasstags(soup,"jobsearch-result")  
                    for txts in category:
                        hreflink = txts.find_all('a', href=True)                    
                        jobsite = hreflink[0].get('href')
                        title = hreflink[0].text  
                        bname = txts.find_all("b")
                        name = bname[0].text
                        dates = txts.find("time").get("datetime")                             
                        extracted = jobsite, name, title, dates 
                        if extracted not in all_linkpage:
                            all_linkpage.append(extracted)     
                            f.write(str(extracted)+"\n")                       
        #logger.error(all_linkpage) 
        #f.close()
        return all_linkpage  
    
    def scrape_contentfromlink(self,links,searchword:str):         
        #db2 = db2database() 
        #ibm_db_conn = ibm_db.pconnect("", "","")
        #conn = ibm_db_dbi.Connection(ibm_db_conn)
        f = open("example_jobdescription.txt","a",encoding="utf-8")
        dataresult = {}          
        count=0 
        for urls in links:     
            url = urls[0].rstrip("\n\r")  
            print(url)        
            if searchword in url and "pdf" not in url:                                            
                time.sleep(1)        
                response = self.requesting_url(url)                
                results = self.get_soup(response)  
                if len(results)>3:
                    tit = urls[2] + urls[3]
                else:
                    tit = urls[2]
                dataresult = self.extract_jobindex(results,url,urls[1],tit,urls[-1],count)   
                
                try:
                    #db2.insert(dataresult,ibm_db_conn) 
                    f.write(str(dataresult)+"\n")
                    print(dataresult)
                except Exception as e:
                    print(e)
                    continue
                except ValueError as e:
                    print(e)
                    continue  
                print(count)
                count+=1                   
            elif "pdf" in url:
                print("pdf file")
            else:
                print("external page ")
                response = self.requesting_url(url)  
                if not response:
                    pass
                else:               
                    results = self.get_soup(response)
                    if len(results)>3:
                        tit = urls[2] + urls[3]
                    else:
                        tit = urls[2]
                    dataresult = self.scrape_externalsites(url,urls[1],tit,urls[-1],count)
                    
                    try:
                        #db2.insert(dataresult,ibm_db_conn) 
                        print(dataresult)
                        f.write(str(dataresult)+"\n")
                    except Exception as e:
                        print(e)
                        continue
                    except ValueError as e:
                        print(e)
                        continue
                    
                    print(count)
                    time.sleep(1)
                    count+=1
        return dataresult   

    def extract_jobindex(self, htmltags,jlink, name, title, dates,count):          
        result = {}    
        bodytext = ""                 
        bodytext = self.get_bodytext(htmltags)                 
        cvr, branch, address, zipcode, city, startdate, employee, profflink = self.middlepage(htmltags,name)   
        if not name or not cvr or not branch or not address or not zipcode or not city or not startdate or not employee:
            print("all the attributes are not extracted")  
        else:     
            result = {"ID":count, "date":dates, "title": title, "text": bodytext,"jobindexlink":jlink,"firmname":name,"cvr":cvr,
            "branch":branch,"address":address,"zipcode":zipcode, "city":city, "startdate":startdate,"employee":employee,"profflink":profflink }                     
            if htmltags=="":                
                print("page is empty")       
        return result

   
    def middlepage(self,htmlsection,name):        
        proffpbj = proffdata()
        cvr, branch, address, zipcode, city, startdate, employee, profflink = "","","","","","","",""
        searchprofflink = ""
        nexturl = ""        
        cprofile = ""
        firminfo = {}
        rooturl = "https://www.jobindex.dk" 
        if self.find_companylink(htmlsection):
            cprofile=self.find_companylink(htmlsection)        
        else:   
            print("no link to middlepage")
            cvr, branch, address, zipcode, city, startdate, employee, profflink = proffpbj.search_proff_by_name(name) 
            return cvr, branch, address, zipcode, city, startdate, employee, profflink           
                    
        nexturl = rooturl + str(cprofile)       
        findnextpage = self.requesting_url(nexturl)             
        newsoup = self.get_soup(findnextpage)
        if not newsoup:
            print("No company info available")        
        else:  
            if self.findallclasstags(newsoup,"col","div"):
                classcol = self.findallclasstags(newsoup,"col","div") 
            else:
                classcol = self.findallclasstags("vp-box","div")             
            if len(classcol)>1:
                classcol = classcol[-1] 
            if classcol.find("a").get("href"): 
                targeturl = classcol.find("a").get("href")  
            if "proff" in str(targeturl): 
                print("found proff") 
                cvr, branch, address, zipcode, city, startdate, employee = proffpbj.get_data_from_proff(targeturl.rstrip("\n\r"))                        
                
                return cvr, branch, address, zipcode, city, startdate, employee, profflink
            else:
                print("there is no link to proff - so searching proff directly by name")
                cvr, branch, address, zipcode, city, startdate, employee, searchprofflink = proffpbj.search_proff_by_name(name)            
                return cvr, branch, address, zipcode, city, startdate, employee, searchprofflink

    def find_companylink(self,htmlsection): 
        cprofile=""
        if self.findclasstag(htmlsection,"vp-card__name","a"):
            cprofile = self.findclasstag(htmlsection,"vp-card__name","a")
            cprofile = cprofile.get('href')
        elif self.findclasstag(htmlsection,"jix_companyprofile_paid","li"):
            cprofile = self.findclasstag(htmlsection,"jix_companyprofile_paid","li") 
            cprofile = cprofile.find("a").get('href') 
        elif self.findclasstag(htmlsection,"jix_companyprofile_unpaid","li"):
            cprofile = self.findclasstag(htmlsection,"jix_companyprofile_unpaid","li") 
            cprofile = cprofile.find("a").get('href')
        return cprofile   
    

    def scrape_externalsites(self, url, name, title, dates, count):
        proff = proffdata()
        result = {}
        text = ""
        response = self.requesting_url(url)         
        if response==None:
            return result
        else:
            htmltags = self.get_soup(response)
            text = htmltags.text               
            text = self.strip_tags_fromtext(text)  
            text = self.remove_letter_n_and_t(text)              
            text = self.split_dot(text)
            text = self.split_fromlowertoupper(text)
            text = self.split_fromupperlower(text)              
            text = text.strip
            cvr, branch, address, zipcode, city, startdate, employee, profflink = proff.search_proff_by_name(name)
            result = {"ID":count, "date":dates, "title": title, "text": text,"joblink":url,"firmname":name,"cvr":cvr,
            "branch":branch,"address":address,"zipcode":zipcode, "city":city, "startdate":startdate,"employee":employee,"profflink":profflink } 
            
            return result   
   
    def get_bodytext(self,section):
        bodytext = ""
        if section.find(class_="col-md-8"):
            tbody = section.find(class_="col-md-8")         
            bodytext = str(tbody)        
        if section.find(id="jobad_jobdetails_description"):
            details = section.find(id="jobad_jobdetails_description")        
            bodytext = details                
        elif section.find(class_="advertise_compact"):
            advertise = section.find(class_="advertise_compact")
            bodytext = advertise
        elif section.find(id="AdvertisementInnerContent"):
            innercontent = section.find(id="AdvertisementInnerContent")
            bodytext = innercontent            
        elif section.find(class_="Div_ViewContainer"):
            btext = section.find(class_="Div_ViewContainer")            
            bodytext = btext 
        elif section.find_all('p'):                
            for textline in section.find_all('p'):                
                bodytext += str(textline)                
        else:
            bodytext +="No text"                                                          
        bodytext = self.strip_tags_fromtext(bodytext) 
        bodytext = self.remove_letter_n_and_t(bodytext)              
        bodytext = self.split_dot(bodytext)
        bodytext = self.split_fromlowertoupper(bodytext)
        bodytext = self.split_fromupperlower(bodytext)

        return bodytext

   