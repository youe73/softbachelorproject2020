import unittest
from unittest.mock import patch
from scraper.scraperclass import Datascraper
from jobindex import Jobindex
from proff import proffdata
from bs4 import BeautifulSoup


class testScrapper(unittest.TestCase):
    def setUp(self):
        print("Set up")
        self.data = Datascraper()
        self.jbindex = Jobindex()
        self.proff = proffdata()
    
    def tearDown(self):
        print("Tear down")  

    # proffclass
    def test_address_decompose(self): 
        print("test get address")       
        addrlist = "Nørgaardsvej 30, 2800 Kongens Lyngby"
        tupadd = ('Nørgaardsvej 30, ', '2800', ' Kongens Lyngby')
        self.assertEqual(self.proff.address_decompose(addrlist),tupadd,"")
        self.assertTupleEqual(self.proff.address_decompose(addrlist),tupadd,"tuple")

    # scraperclass
    def test_remove_letter_n_and_t(self):
        print("test remove letter n and t")
        text = "nThis nGreat"
        self.assertEqual(self.data.remove_letter_n_and_t(text),"This Great","")
        self.assertEqual(self.data.remove_letter_n_and_t("hi t t"),"hi  ","")
        self.assertEqual(self.data.remove_letter_n_and_t("hi n "),"hi  ","")
        self.assertEqual(self.data.remove_letter_n_and_t("nhi"),"nhi","")
        self.assertNotEqual(self.data.remove_letter_n_and_t("nhi"),"hi","")

    def test_split_fromupperlower(self):
        print("test separate words capital letters")
        expected = "I am attending CBS. This is what I learn in BUSINESS. And I will finish soon"
        text = "I am attending CBSThis is what I learn in BUSINESSAnd I will finish soon"
        expected2 = "FEDT. Det er god"
        text2 = "FEDTDet er god"
        self.assertEqual(self.data.split_fromupperlower(text),expected,"")
        self.assertEqual(self.data.split_fromupperlower(text2),expected2,"")
        
    
    def test_split_dot(self):
        print("test split text with dot")
        expected = "god dag. Jeg synes det er varmt. Måske vi"
        text = "god dag.Jeg synes det er varmt.Måske vi"
        expected2 = "det. er fint"
        text2 = "det.er fint"
        self.assertEqual(self.data.split_dot(text),expected,"")
        self.assertNotEqual(self.data.split_dot(text2),expected2,"")

    def test_split_fromlowertoupper(self):
        print("test split from lower to upper")
        expected = "kan Produktionschef"
        text = "kanProduktionschef"
        self.assertEqual(self.data.split_fromlowertoupper(text),expected,"")       


    def test_larger_thanthree(self):
        print("test larger than three")
        text = "three"
        text2 = "is"
        expected = ["three"]
        expected2 = []
        self.assertListEqual(self.data.larger_thanthree(text),expected)
        self.assertListEqual(self.data.larger_thanthree(text2),expected2)
        
    def test_findallclasstags(self):
        print("test find all tagkind")
        text = """<div class="thisid"><p>This is main</p></div>"""
        soup = BeautifulSoup(text, "html.parser")
        self.assertTrue(self.data.findallclasstags(soup,"thisid","div"),list)
        self.assertEqual(self.data.findallclasstags(soup,"wrongid","div"),[])

    def test_findclasstags(self):
        print("test find class tags")
        text = """<div class="thisid">This is main</div>"""
        soup = BeautifulSoup(text, "html.parser")
        result = self.data.findclasstag(soup, "thisid","div")
        result2 = self.data.findclasstag(soup, "wrongid","div")
        self.assertEqual(result.text,"This is main","")
        self.assertEqual(result2,None,"")

    def test_remove_duplicate_links(self):
        print("test remove duplicate links")
        old_link =[1,2,3,4,4,4,6,7,7,8,8,9]        
        new_link=[1,2,3,4,6,7,8,9]    
        self.assertEqual(self.data.remove_duplicate_links(old_link),new_link,"") 

    def test_strip_tags_fromtext(self):
        print("test strip tags from text")
        text = "<code><span class='kn'>import</span>"
        result = "import"
        text2 = "import\n\n"
        self.assertEqual(self.data.strip_tags_fromtext(text),result)
        self.assertEqual(self.data.strip_tags_fromtext(text2),"import ")

    

if __name__=="__main__":
    unittest.main()
    #python -m unittest -v unittest_scraper.py
    #coverage run unittest_scraper.py
    #coverage report