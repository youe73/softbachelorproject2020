from pymongo import MongoClient
from pprint import pprint

class mongo():   

    try:       
        client = MongoClient('localhost', 27018)       
        
    except Exception as e:
        print("Cannot connect to MongoDB" , e)
    
     
	#databases and collections used
	
    #db: firms, col: firmlist
    #db: jobindexfirms, col: jobindexlist        
    
    #db = client.jobindexfirms # jobindex's firms are stored
    #col = db.jobindexlist 

    #db = client.firms #proffs firms are stored
    #col = db.firmlist      

    #important
    #db = client.jobadvertisment # jobindex +  external jobads is stored
    #col = db.jobdata

    #db = client.jobindex # jobindex jobannoncer er lagret
    #col = db.jobindex_advertisment

    #db = client.db2content
    #col = db.fromdb2

    #db = client.citynames
    #col = db.cities

    #db = client.db2firmnames
    #col = db.firmnamesfromdb2

    #db = client.country
    #col = db.countrynames

    #db = client.danishfirms
    #col = db.danisfirmnames
    	
    
    def dbinfo(self):
        return self.db

    def colinfo(self):
        return self.col   
    
    def insert(self,article):
        result = self.col.insert_one(article)       
        print("DB insert " , self.col.count())
        return result

    def select_one(self):
        onepost = self.col.find_one()
        return onepost

    def drop_col(self):       
        return self.col.drop()

    def count_doc(self):
        return self.col.count()

    def select_all(self):
        return self.col.find()  

    def select_all_by_id(self,id):
        return self.col.find({"ID":id})
    
    def select_all_by_id_range(self,start, end):
        return self.col.find({"ID":{"$gt":start,"$lt":end}})

    def select_by_name(self,name):
        return self.col.find({"Name":name})

    def search_by_word(self,word): 
        return self.col.find({ "Name": { "$regex": word }}) 

    def search_jobads_by_firmname(self,word): 
        return self.col.find({ "title": { "$regex": word }})

if __name__ == "__main__":
    
    m = mongo()       

    print(m.dbinfo())
    print(m.count_doc())    
    
    cursor = m.client.list_databases()
    for db in cursor:
        print(db)
    
    