import requests
import time
from datetime import date
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
import re
import codecs
import os.path
import logging
from database import mongo
import re



logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) 
formats = logging.Formatter('%(asctime)s:%(name)s:%(message)s:%(levelname)s:%(lineno)d')

file_handler = logging.FileHandler('./scraper/debug_logfil.log',mode='w')
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formats)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formats)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

class Datascraper:

    useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
    headers = {'User-Agent': useragent}

    def requesting_url(self,url):   
        session = requests.Session()
        adapter = HTTPAdapter(max_retries=3)   
        session.mount(url,adapter)  
        try:
            response = session.get(url,headers=self.headers ,timeout=5) 
        except requests.exceptions.Timeout as e:
            logger.exception("timeout",e)           
        except requests.exceptions.ConnectionError as e:
            logger.exception("Connection error")        
        except requests.exceptions.TooManyRedirects as e:
            logger.exception("bad request", e)
        except requests.exceptions.RequestException as e:
            logger.exception("request problem", e)  
        except requests.exceptions.SSLError as e:
            logger.exception("Verification problem",e)   
        else:    
            session.close()        
            return response   

    def get_soup(self,response):      
        soup = ""
        try:
            soup = BeautifulSoup(response.text, "html.parser")
        except Exception as e:
            print(e, "cannot scrape this page")
            return 
        else:  
            return soup

    def htmlpage(self,url):
        response = self.requesting_url(url)
        soup = self.get_soup(response)
        return soup

    def remove_duplicate_links(self, link):
        finish_link = list(dict.fromkeys(link))
        return finish_link    

    def strip_tags_fromtext(self,bodytext):
        
        bodytext = re.sub(r'<.*?>', '',str(bodytext))
        bodytext = re.sub(r'\n\s*\n', ' ', bodytext)       
        bodytext = re.sub(r'\t\s*', ' ', bodytext)
        bodytext = bodytext.replace("\n"," ")
        bodytext = bodytext.replace("\r"," ")     
        bodytext = bodytext.replace("•", " ") 
        bodytext = bodytext.replace("   ","") 
        return bodytext         
       
    def remove_letter_n_and_t(self,text):        
        strarr2=text.split(" ")
        newlist2 = []
        newstr2 = ""        
        for i2 in strarr2:    
            if "n" in i2: 
                match2 = re.search("n",i2)
                pos2 = match2.span()
                first2 = pos2[0]
                second2 = pos2[1]          
                if i2[0] == "n": 
                    if len(i2)>1:
                        if i2[1].isupper(): #if first occurence of letter n is followed by any capital letter.                             
                            newlist2.append(i2[:first2]+i2[second2:])     
                        elif i2[1].isdigit():                
                            newlist2.append(i2[:first2]+i2[second2:])                                    
                        else:
                            newlist2.append(i2)                    
                    elif len(i2)==1: # it is only one letter...it means a single n               
                        newlist2.append(i2[:first2]+i2[second2:])
                    else:
                        newlist2.append(i2)                        
                else:
                    newlist2.append(i2)    
            elif "t" in i2:
                match = re.search("t",i2)
                pos_t = match.span()
                firstt = pos_t[0]
                secondt = pos_t[1] 
                if i2[0]=="t":
                    if len(i2)>1:
                        if i2[1].isupper():
                            newlist2.append(i2[:firstt]+i2[secondt:])
                        elif i2[1].isdigit():                     
                            newlist2.append(i2[:firstt]+i2[secondt:])                                   
                        else:
                            newlist2.append(i2)                    
                    elif len(i2)==1:               
                        newlist2.append(i2[:firstt]+i2[secondt:]) 
                else:
                    newlist2.append(i2)          
            else:
                newlist2.append(i2)
        newstr2 = " ".join(newlist2)
        return newstr2     
   
   

    def mongo_to_csv(self,filename):
        db = mongo()
        query = db.select_all()
        idarr,datesarr,titlearr,textarr = [],[],[],[]
        for q in query:
            idarr.append(q["ID"])
            datesarr.append(q["date"])
            titlearr.append(self.remove_letter_n_and_t(self.strip_tage_titel(q["title"])))
            textarr.append(self.remove_letter_n_and_t(self.strip_tags_fromtext(q["text"])))
            print(q["ID"])    
        self.combinesources(idarr,datesarr,titlearr,textarr,filename)

    def combinefiles(self,path,csvfile):
        csvfile = csvfile + ".csv"
        all_files = []
        for filename in os.listdir(path):            
            file_path = os.path.join(path, filename)            
            all_files.append(file_path)
        all_csv = pd.concat([pd.read_csv(f) for f in all_files ])
        all_csv.to_csv(csvfile, index=False, encoding='utf-8-sig') #utf-8-sig is a signature 
        return ""
        
    def combinesources(self,idarr,datesarr,titlearr,textarr,csvfilename):
        csvfilename = csvfilename + ".csv"
        frame = {"ID":idarr,"Date":datesarr, "Title":titlearr, "Text":textarr}      
        df = pd.DataFrame(frame)
        df.to_csv(csvfilename, encoding='utf-8') 

    def csv_format(self,data,csvfilename):
        csvfilename = csvfilename + ".csv" 
        if data["firminfo"]!="":
            firminfo = data["firminfo"] 
        else:
            firminfo = "None"
        frame = {"ID":data["ID"], "date":data["date"], "title": data["title"], "text": data["text"],"jobindexlink":data["jobindexlink"],"source":None,
        "name":firminfo["name"], "cvr":firminfo["cvr"],"address":firminfo["address"], "zip":firminfo["zip"], "city":firminfo["city"],"startdate":firminfo["startdate"],
        "employee": firminfo["employee"],"profflink":firminfo["profflink"]}      
        df = pd.DataFrame(frame)
        df.to_csv(csvfilename, encoding='utf-8')
                   
    def findclasstag(self, soup, classname, tagtype="" ):        
        try:
            soup.find(tagtype, class_=classname)
        except Exception as e:
            print(e, "This class tag does not exist")
        else:            
            return soup.find(tagtype, class_=classname)

    def findallclasstags(self, soup, classname, tagtype="" ):    
        try:
            soup.find_all(tagtype, class_=classname)
        except Exception as e:
            print(e, "These class tags does not exist")
        else:            
            return soup.find_all(tagtype, class_=classname)
   

    def larger_thanthree(self,word:str):
        corpus = []
        if len(word)>3:
            corpus.append(word)
        return corpus    
    
        
    def wordstart(self,words):
        wordarr = []
        worddict = {}
        i = 0
        for w in words:
            if w == ".":            
                wordict = {"id":i,"letter":words}            
            i+=1
        return wordict["id"]

    def split_dot(self,text):           
        strarr=text.split(" ")
        newlist = []
        newstr = ""        
        for i in strarr:    
            if "." in i: 
                start = self.wordstart(i)
                end = start+1                                      
                l = len(i)            
                #print(i2[start:end])            
                if i[start:end+1].isupper():                 
                    separated = i[:start] + ". " + i[end:]
                    newlist.append(separated) 
                else:
                    newlist.append(i)    
            else:
                newlist.append(i)
        newstr = " ".join(newlist)
        return newstr
    
        
    def split_fromlowertoupper(self,word):
        count = 0
        final = []
        wordstr = ""
        for w in word:
            if w.isupper() and word[count-1:count].islower():  
                space =  " "  + w        
                final.append(space)            
            else:            
                final.append(w)                
            count+=1
        wordstr = "".join(final)
        return wordstr

    def split_fromupperlower(self,word):    
        sen = []
        normal = []
        final = []
        splitword = ""
        count = 0
        for w in word:   
            sen.append(w)  
            if w.isupper():
                pre = word[count-1:count]
                after = word[count+1:count+2]
                if pre==" " or after==" ":                
                    final.append(w)           
                elif after.isupper():                
                    final.append(w)
                elif after.islower():                
                    root = ". " + w 
                    final.append(root)
                elif after.isnumeric():                
                    root = w + ". "
                    final.append(root)
            else:
                final.append(w)                        
            count+=1
        wordstr = "".join(final)
        return wordstr