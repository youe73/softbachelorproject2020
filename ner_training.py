from __future__ import unicode_literals, print_function
import pandas as pd
import re
import time
from sklearn.pipeline import Pipeline
import sys
from pymongo import MongoClient
import spacy
from spacy import displacy
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher
import datetime as d
import plac
import random
import warnings
from pathlib import Path
from spacy.tokens import Span
from tqdm import tqdm
from spacy.util import minibatch, compounding

openeddataframe = pd.read_csv("./data/cleaneddata.csv", encoding='utf-8')

# totalfirms is the result of scraped firmnames +- some extra firmnames
newfirmnames = []
for firm in firmnames:    
    if "DANMARK" in str(firm):        
        f = re.sub(r'DANMARK','',str(firm))
        f = f.replace("  "," ")
        newfirmnames.append(f)
    elif "Danmark" in str(firm):        
        f = re.sub(r'Danmark','',str(firm))
        f = f.replace("  "," ")        
        newfirmnames.append(f)
    elif "DENMARK" in str(firm):        
        f = re.sub(r'DENMARK','',str(firm))
        f = f.replace("  "," ")
        newfirmnames.append(f) 
    elif "Denmark" in str(firm):        
        f = re.sub(r'Denmark','',str(firm))
        f = f.replace("  "," ")
        newfirmnames.append(f) 
    else:
        newfirmnames.append(firm)


newfirmnames2 = []
for firm in newfirmnames: 
    if "K/S" in str(firm):        
        f = re.sub(r'K/S','',str(firm))
        f = f.replace("  "," ")
        newfirmnames2.append(f)
    elif "A/S" in str(firm):        
        f = re.sub(r'A/S','',str(firm))
        f = f.replace("  "," ")
        newfirmnames2.append(f)
    elif "ApS" in str(firm):        
        f = re.sub(r'ApS','',str(firm))
        f = f.replace("  "," ")
        newfirmnames2.append(f) 
    elif "P/S" in str(firm):        
        f = re.sub(r'P/S','',str(firm))
        f = f.replace("  "," ")
        newfirmnames2.append(f) 
    else:
        newfirmnames2.append(firm)
           
newfirmnames3 = []
for firm in newfirmnames2: 
   
    if "A.M.B.A." in str(firm):        
        f = re.sub(r'A.M.B.A.','',str(firm))
        f = f.replace("  "," ")
        newfirmnames3.append(f)
    elif "filial" in str(firm):        
        f = re.sub(r'filial','',str(firm))
        f = f.replace("  "," ")
        newfirmnames3.append(f)
    elif "Holdings" in str(firm):        
        f = re.sub(r'Holdings','',str(firm))
        f = f.replace("  "," ")
        newfirmnames3.append(f)
    elif "FORSIKRING" in str(firm):        
        f = re.sub(r'FORSIKRING','',str(firm))
        f = f.replace("  "," ")
        newfirmnames3.append(f)
    elif "AKTIESELSKAB" in str(firm):        
        f = re.sub(r'AKTIESELSKAB','',str(firm))
        f = f.replace("  "," ")
        newfirmnames3.append(f)
    elif "STATSAUTORISERET REVISIONSPARTNERSELSKAB" in str(firm):        
        f = re.sub(r'STATSAUTORISERET REVISIONSPARTNERSELSKAB','',str(firm))
        f = f.replace("  "," ")
        newfirmnames3.append(f)
    else:
        newfirmnames3.append(firm)
           
firms = []
for a in newfirmnames3:
    if len(a.split(" "))==2:
        if a.split(" ")[-1]=="kommune" or a.split(" ")[-1]=="Kommune" or a.split(" ")[-1]=="KOMMUNE":
            firms.append(a.split(" ")[-1])
        else:
            firms.append(a)
    
firmsimple = []
for a in firms:
    if len(a.split(" "))==2:        
        part = a.split(" ")
        if part[1]!="":
            unit = part[0]+ "-" + part[1]
            firmsimple.append(unit)
        else:
            firmsimple.append(part[0])            
    else:
        firmsimple.append(a)
        

textframe = []
for x in openeddataframe.Text:
    if type(x) != float:
        textframe.append(x)

hardskill = ["bachelor","Bachelor","CM","Kandidat","Cand Merc","cand merc","Cand.merc.","Cand. Merc.","cand ","HA","PBA","engelsk","merkonom","ingeniør","markedsføringsøkonom","It","master","management","finansiering","marketing","marketing","salg","matematik","programmering","software","hardware","BI","Business Intelligence"]
softskill = ["ambitiøs","analytisk","ansvarlig","brænde","drive","dygtig","dynamisk","engagere","erfaring","faglig","formidle","international","kompetence","kreativ","lede","motivere","kommunikere","tålmodig","Som person","evner","empati","empatisk","initiativrig","initiativtager","selvstændig","selvkørende","egenskaber","selvmotiverende","fleksibel","udadvendt","ejerskab","omstillingsparat"]
techskill = ["php","java","javascript","python","c#",".net","asp.net","golang","c++","visual basic","typescript","cython","excel","mysql","sql","unittest","junit","ci/cd","powerbi","azure","Data Science","cloud","robotic","iot","server administrator"]

nlp = spacy.load("da_core_news_sm")

matcher = PhraseMatcher(nlp.vocab)

patterns = [nlp.make_doc(text) for text in hardskill]
patterns2 = [nlp.make_doc(text) for text in softskill]
patterns3 = [nlp.make_doc(text) for text in totalfirms]
patterns4 = [nlp.make_doc(text) for text in techskill]

matcher.add("hard", None, *patterns)
matcher.add("soft", None, *patterns2)
matcher.add("firms", None, *patterns3)
matcher.add("techskill", None, *patterns4)


def createannotations(text):
    hardannotations = []
    softannotations = []
    firms = []
    technicalskill = []
    
    city = []
    country = []
        
    doc = nlp(text)
    matches = matcher(doc)  
    for match_id, start, end in matches:        
        span = doc[start:end]         
        if span.text in hardskill:             
            annotation = "hardskill"           
            hardannotations.append((doc[start:end].start_char,doc[start:end].end_char,annotation))            
            
        elif span.text in softskill:            
            annotation = "softskill"
            softannotations.append((doc[start:end].start_char, doc[start:end].end_char,annotation))
            
        elif span.text in totalfirms:
            annotation = "firmname"
            firms.append((doc[start:end].start_char, doc[start:end].end_char,annotation))
            
        elif span.text in techskill:
            annotation = "techskill"
            technicalskill.append((doc[start:end].start_char, doc[start:end].end_char,annotation))
            
      
    
    hardannotations = remove_duplicate_links(hardannotations)
    softannotations = remove_duplicate_links(softannotations)
    firms = remove_duplicate_links(firms)
    technicalskill = remove_duplicate_links(technicalskill)
   
    
    subannotations = hardannotations + softannotations + firms +technicalskill 
    return (doc.text, {'entities': subannotations})

#creating trainin data
Traindata = []
count = 0
for txt in textframe:
    Traindata.append(createannotations(txt))
    print(count)
    count+=1


output_dir=Path("./ner_models")
n_iter = 20

# this part of code is taken directly from Spacy documentation
#https://spacy.io/usage/training
if 'ner' not in nlp.pipe_names:
    ner = nlp.create_pipe('ner')
    nlp.add_pipe(ner, last=True)
else:
    ner = nlp.get_pipe('ner')

# this part of code is taken directly from Spacy documentation
#https://spacy.io/usage/training
# minibatch
for _, annotations in Traindata:
    for ent in annotations.get('entities'):
        ner.add_label(ent[2])

# not training a new model but using the nlp - danish version 
for itn in range(n_iter):
    random.shuffle(Traindata)
    losses = {}    
    batches = minibatch(Traindata, size=compounding(4.0, 32.0, 1.001))
    for batch in batches:
        texts, annotations = zip(*batch)
        nlp.update(
            texts,  
            annotations,  
            drop=0.5,  
            losses=losses,
        )
    print("Losses", itn, losses, d.datetime.now())
