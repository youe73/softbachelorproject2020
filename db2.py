import ibm_db
import codecs
import os.path
import re
import ibm_db_dbi
from scraper.scraperclass import Datascraper
from bs4 import BeautifulSoup
from database import mongo
import datetime
from dateutil.parser import parse

class db2database():    

    try:
        ibm_db_conn = ibm_db.connect("", "", "")
    except ConnectionError as e:
        print(e)
    
    print("Connection ok", ibm_db_conn)
    conn = ibm_db_dbi.Connection(ibm_db_conn)  
    c = conn.cursor()
    

    def connect_verification(self):
        return self.ibm_db_conn
    
        
    def get_firmnames(self,c, mongo):        
        dicts = {}
        c.execute(f"select FIRMNAME FROM JOBINDEX")
        rows = c.fetchall()   
        for lines in rows: 
            if lines !="":                
                dicts = {"firmname":lines}
                mongo.insert(dicts)
                print("inserted", lines)
        c.close()
        return "done" 
    

    def insert(self,data,ibm_db_conn):    
        try:
            id = data["ID"]
        except Exception as e:
            print("ID", e)
        
        try:
            if data["date"]:
                dates = data["date"].rstrip("\n")
                dates = dates.strip()
                dates = dates.lstrip()                
                date_time = datetime.datetime.strptime(dates,'%Y-%m-%d') #:%S #%H:%M             
                thedates = date_time.date() 
            else:
                thedates = ""        
        except Exception as e:
            print("date", e)            
            pass
        try:
            title = data["title"].strip()
            title = title.rstrip("\n")
        except Exception as e:
            print("title",e)
            title = ""
        try:
            text = data["text"].strip()            
        except Exception as e:
            print("Text",e)            
        try:
            joblink = data["joblink"].strip()
            joblink = joblink.rstrip("\n")                
            joblink = re.sub(r'<.*?>', ' ',joblink)            
            joblink = joblink.encode('utf-8')
        except Exception as e:
            print("joblink",e)
            joblink = ""
        try:
            firmname = data["firmname"].strip()
            firmname = firmname.rstrip("\n")
        except Exception as e:
            print("firmname",e)
            firmname =""

        try:
            cvr = data["cvr"].strip()
            cvr = cvr.rstrip("\n")
        except Exception as e:
            print("cvr",e)
            cvr = ""

        try:
            branch = data["branch"].strip()
            branch = branch.rstrip("\n")            
            if len(str(branch))>128:
                branch = branch[0:120]
        except UnicodeDecodeError as e:
            print("branch",e)
           
        try:
            address = data["address"].strip()
            address = address.rstrip("\n")
        except Exception as e:
            print("Address",e)
            address = ""

        try:
            zipcode = data["zipcode"].strip()
            zipcode = zipcode.rstrip("\n")
        except Exception as e:
            print("Zipcode",e)
            zipcode=""

        try:
            city = data["city"].strip()
            city = city.rstrip("\n")
        except Exception as e:
            print("City",e)
            city=""
        
        try:
            if data["startdate"]:
                startdate = data["startdate"].rstrip("\n")            
                startdate = startdate.strip()
                startdate = startdate.lstrip()
                
                date_time = datetime.datetime.strptime(startdate,'%d-%m-%Y') #:%S #%H:%M             
                startdate = date_time.date() 
            else:
                startdate =""
        except Exception as e:
            print("Startdate",e)
        
        try:
            employee = data["employee"].strip()
            employee = employee.rstrip("\n")
        except Exception as e:
            print("employee",e)
            employee=""

        try:
            profflink = data["profflink"].strip()
            profflink = profflink.rstrip("\n")
        except Exception as e:
            print("Profflink",e)
            profflink = ""        
               
            
        """
        insert_sql="insert into JOBINDEX values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        stmt = ibm_db.prepare(ibm_db_conn, insert_sql)
        ibm_db.bind_param(stmt, 1, id)
        ibm_db.bind_param(stmt, 2, thedates)
        ibm_db.bind_param(stmt, 3, title)        
        ibm_db.bind_param(stmt, 4, text)
        ibm_db.bind_param(stmt, 5, joblink)
        ibm_db.bind_param(stmt, 6, firmname)
        ibm_db.bind_param(stmt, 7, cvr)
        ibm_db.bind_param(stmt, 8, branch)    
        ibm_db.bind_param(stmt, 9, address)
        ibm_db.bind_param(stmt, 10, zipcode)
        ibm_db.bind_param(stmt, 11, city)
        ibm_db.bind_param(stmt, 12, startdate)
        ibm_db.bind_param(stmt, 13, employee)
        ibm_db.bind_param(stmt, 14, profflink)

                
        try:
            ibm_db.execute(stmt)  
            print(id, "Inserted into DB2")                  
        except Exception as e:
            print("***executionerror ",ibm_db.stmt_errormsg(),e)                                     
        except ValueError as e:
            print("***value error ",e)  
        except UnicodeDecodeError as e:
            print("***unicode error")
            
        """
    
