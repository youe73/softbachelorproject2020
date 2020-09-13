import unittest
from unittest.mock import patch, Mock
from scraper.scraperclass import Datascraper
from jobindex import Jobindex
from proff import proffdata
#from database import mongo
#from db2 import db2database
from bs4 import BeautifulSoup
from requests.exceptions import Timeout

class integrationstest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print("Set up") 
        
        cls.crawl = Datascraper()
        cls.jobindex = Jobindex()       
        cls.proff = proffdata()   
        #cls.db2 = db2database()
        
        cls.catlist = ['https://www.jobindex.dk/job/it', 'https://www.jobindex.dk/job/ingenioer', 'https://www.jobindex.dk/job/ledelse', 
        'https://www.jobindex.dk/job/handel', 'https://www.jobindex.dk/job/industri', 'https://www.jobindex.dk/job/salg', 
        'https://www.jobindex.dk/job/undervisning', 'https://www.jobindex.dk/job/kontor', 'https://www.jobindex.dk/job/social', 
        'https://www.jobindex.dk/job/oevrige']
        
        cls.area_list=["/jobsoegning/it/systemudvikling/storkoebenhavn","/jobsoegning/it/systemudvikling/nordsjaelland","/jobsoegning/it/systemudvikling/region-sjaelland"]
        cls.topicarealist = ['https://www.jobindex.dk/jobsoegning/it/systemudvikling/storkoebenhavn', 'https://www.jobindex.dk/jobsoegning/it/systemudvikling/nordsjaelland', 'https://www.jobindex.dk/jobsoegning/it/systemudvikling/region-sjaelland']
        
        cls.entirelist=[('https://jobs.dsv.com/job/Hedehusene-Enterprise-Security-Architect/616683301/?locale=en_US', 'DSV', 'Enterprise Security Architect', '2020-08-26'),
        ('https://pandoragroup.com/careers/vacancies/europe/denmark/delivery-manager-consumer-technology', 'PANDORA A/S', 'Delivery Manager, Consumer Technology', '2020-08-26'),
        ('https://www.danskebank.com/da-dk/karriere/soeg-job/Pages/JobShow.aspx?JobPostingId=20922', 'Danske Bank', 'Head Regulatory Data Analytics & Reporting - Group Compliance, Group Compliance', '2020-08-26')]

        cls.entirelistone=[('https://www.danskebank.com/da-dk/karriere/soeg-job/Pages/JobShow.aspx?JobPostingId=20922', 'Danske Bank', 'Head Regulatory Data Analytics & Reporting - Group Compliance, Group Compliance', '2020-08-26')]
        cls.externpageurl = 'https://www.danskebank.com/da-dk/karriere/soeg-job/Pages/JobShow.aspx?JobPostingId=20922'

        cls.baseurl = "https://www.jobindex.dk/"
       
        cls.url = "https://www.jobindex.dk/jobannonce/366047/field-technical-support-engineer-indflydelse-via-engagement"
        cls.resp = cls.crawl.requesting_url(cls.url)
        cls.basesoup = cls.crawl.get_soup(cls.resp)
        
        cls.proff_url = "https://www.proff.dk/firma/-/-/-/GTUFBQI002C'"
        cls.proff_response = cls.crawl.requesting_url(cls.proff_url)
        cls.proff_soup = cls.crawl.get_soup(cls.proff_response)        
        cls.officiel = cls.proff_soup.find(class_="panel official-info")        
        cls.li = cls.proff_soup.find_all('li',class_="clear")

        cls.firm = {'name': 'Urbaser A/S', 'cvr': '32660533', 'address': 'Erhvervsparken 17', 'zip': ' 4621', 'city': ' Gadstrup', 
        'startdate': '22-12-2009', 'employee': '500 - 999', 'profflink': 'https://www.proff.dk/firma/-/-/-/GTUFBQI002C'}

            
    @classmethod
    def tearDownClass(cls):
        print("Tear down")    
   
    @patch("jobindex.Jobindex",return_value=200)    
    def test_request_url_object(self,mockrequest):
        print("testing request")       
        mockrequest.requesting_url.response=200  
        mockrequest.requesting_url(self.baseurl)
        mockrequest.requesting_url.assert_called_once()   
             
    @patch("jobindex.Jobindex.get_root_links",return_value=list)
    def test_get_root_links(self,mockrequest):
        print("test get rootlinks")                
        mockrequest.get_root_links.return_value = list
        mockrequest.get_root_links(self.baseurl)        
        self.assertEqual(mockrequest.get_root_links.return_value,self.jobindex.get_root_links(self.baseurl))

    @patch("jobindex.Jobindex.getall_topic_links", return_value=102)
    def test_getall_topic_links(self,mockrequest):
        print("test get all topics links")  
        mockrequest.getall_topic_links.return_value=102       
        self.assertEqual(mockrequest.getall_topic_links.return_value,self.jobindex.getall_topic_links(self.catlist,self.baseurl))

    
    @patch("jobindex.Jobindex.get_all_area", return_value=1326)
    def test_get_all_area(self, mockrequest):
        print("test get all area")
        mockrequest.get_all_area.return_value=1326
        listlen = self.jobindex.get_all_area(self.jobindex.getall_topic_links(self.catlist,self.baseurl))
        self.assertEqual(mockrequest.get_all_area.return_value,listlen)
    
    @patch("jobindex.Jobindex.make_topic_area_page",return_value=list)
    def test_make_topic_area_page(self, mockrequest):
        print("test make topic area")
        mockrequest.make_topic_area_page.return_value=list
        areatopicurl = self.jobindex.make_topic_area_page(self.area_list,self.baseurl)
        self.assertEqual(mockrequest.make_topic_area_page.return_value, areatopicurl)

    @patch("jobindex.Jobindex.get_all_links", return_value=list)
    def test_get_all_links(self,mockrequest):
        print("testing get all links")      
        mockrequest.get_all_links.return_value=list
        value = self.jobindex.get_all_links(self.topicarealist,"?page=")
        self.assertEqual(mockrequest.get_all_links.return_value,value) 
    
    @patch("jobindex.Jobindex.get_all_links")
    @patch("jobindex.Jobindex.scrape_contentfromlink", return_value=dict)
    def test_scrape_contentfromlink(self,mocklinks, mockcontent):
        print("test scrape content from link")
        mocklinks.get_all_links.return_value=self.entirelist        
        mockcontent.scrape_contentfromlink.return_value=dict
        result = self.jobindex.scrape_contentfromlink(mocklinks.get_all_links.return_value,"jobindex.dk")        
        self.assertEqual(mockcontent.scrape_contentfromlink.return_value,result)

    def test_scrape_contentfromlink2(self):
        print("test scrape content from link2")
        data = self.jobindex.scrape_contentfromlink(self.entirelistone,"jobindex")
        self.assertTrue(data,dict)

    @patch("database.mongo", return_value=27017)
    def test_mongo_database_connection(self,mockrequest):
        print("testing mongodb")
        port = mockrequest.MongoClient.PORT = 27017 
        mockrequest.mongodb.dbinfo()
        mockrequest.mongodb.dbinfo.assert_called_once()     
       
    """
    @patch("db2.db2database.connect_verification", return_value=object)
    def test_DB2_connection(self, mockrequest):
        print("test DB2 connection")
        resp =mockrequest.connect_verification.return_value=object  
        db = self.db2.connect_verification()     
        self.assertIsInstance(resp,db)      
        self.assertEqual(resp,db)  
    """

    def test_requesturl(self):
        print("testing request url")       
        self.assertIsNotNone(self.resp)
        self.assertTrue(self.resp.status_code,200)

    def test_soup(self):
        print("test soup")  
        self.assertNotEqual(self.basesoup,"cannot scrape this page")
    
    def test_get_data_from_proff(self):
        print("test get data from proff") 
        for listtag in self.li:
            self.assertEqual(self.crawl.get_data_from_proff(listtag),(self.firm['name'], self.firm['cvr'], self.firm['address'], self.firm['zip'], self.firm['city'], self.firm['startdate'], self.firm['employee']),"")
                    
    def test_search_proff_by_name(self):
        print("test search proff by name ")
        name = "ifm electronic"
        result = self.proff.search_proff_by_name(name)
        exp = {'name': 'IFM Electronic A/S', 'cvr': '21409286', 'address': 'Ringager 4 A 1 tv', 'zip': ' 2605', 'city': ' Brøndby', 
                'startdate': '01-10-1998', 'employee': '10 - 19', 'profflink': 'https://www.proff.dk/firma/ifm-electronic-as/br%C3%B8ndby/elektronik-og-telekommunikationsudstyr-engros/GMHE6GI10MZ/'}
        self.assertTrue(result,exp)

    def test_extract_jobindex(self):
        print("test extract jobindex page")   
        name = "IFM Electronic A/S"
        title = "Field technical support engineer – indflydelse via engagement!"
        dates = "2020-08-26"
        count = 25      
        response = self.jobindex.extract_jobindex(self.basesoup,self.url,name, title, dates,count)             
        self.assertTrue(response,dict)

    def test_middlepage(self):
        print("test get middlepage")
        name = "IFM Electronic A/S"
        result = self.jobindex.middlepage(self.basesoup, name)
        self.assertTrue(result,list)

    def test_find_companylink(self):
        print("test find companylink")
        result = self.jobindex.find_companylink(self.basesoup)
        exp = "/virksomhed/42324/ifm-electronic-a-s"
        self.assertTrue(result,exp)

    def test_scrape_externalsites(self):
        print("test scrape externalsites")
        name = "Danske Bank"
        title = "Head Regulatory Data Analytics & Reporting - Group Compliance, Group Compliance"
        dates = "2020-08-26"
        count = 30
        result = self.jobindex.scrape_externalsites(self.externpageurl, name, title, dates, count) 
        self.assertTrue(result,dict)

    def test_get_bodytext(self):
        print("test get bodytext")        
        self.assertIsNotNone(self.jobindex.get_bodytext(self.basesoup))

    
   
if __name__=="__main__":
    unittest.main()   
    
    #coverage run integrationtest.py   
    #coverage report -m