import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import text 
from sklearn.decomposition import LatentDirichletAllocation
import pickle
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.stem import SnowballStemmer
import re
import nltk
import time
from pymongo import MongoClient

stemmer = SnowballStemmer("danish")
df = pd.read_csv("comlete_danish_documents2.csv", encoding="utf-8")

# the loading of data is time consuming and it has been loaded from mongodb to increase the speed.
# This is the majority of the XMLDB2 data.

try:
    client = MongoClient('localhost', 27017)
except Exception as e:
    print("Cannot connect to MongoDB" , e)
else:
    #db = client.cleaned 
    #col = db.articlecol

frame = {}
idarr = []
daarr = []
query = col.find()
for data in query:
    idarr.append(data["ID"])
    daarr.append(data["da"])
frame = {"ID":idarr, "da": daarr }

df = pd.DataFrame(frame)

def remove_three(w):
    if len(w)>3:
        return w

df['cured'] = [[remove_three(w) for w in row] for row in df['da']]
df['result'] = [''.join(str(s)) for s in df["result"]]

danishstopwords = nltk.corpus.stopwords.words('danish')
f = open("stopord.txt", "r", encoding="utf-8")
finn = f.readlines()
finnlist = []
for l in finn:
    finnlist.append(l.rstrip("\n"))  

danishstopwords.extend(finnlist)
extras = ["facebook", "ofir", "cookies","klik","dokumenter","cv", "jobannonce", "job","søg",
          "jobindex","dk","computerworld","jobbank","dk","kl","stillingersøg", "antal", "mail", "læs", "ansøgning", "online",
         "ca", "stillinger", "inden","pr","link", "pl","ledige", "jobbet", "søges", "pr", "uge", "afdelingen","tlf",
         "lønog","ansøgningsfrist","august","send","bl","mandag","yderligere","ansættelse","ansættelsessamtaler",
          "ansættelsesvilkår","ansættelsesforhold","arbejdet","evt","følgende","None"]
danishstopwords.extend(extras)
len(danishstopwords)

df['cured'] = [[remove_three(w) for w in row] for row in df['da']]
curedtext = df.cured
text = [''.join(str(s)) for s in curedtext]

#countvectorizer
countvectorizer = CountVectorizer(stop_words=danishstopwords, min_df=0.1, max_df=0.70, max_features=5000)
vectortransformed = countvectorizer.fit_transform(text)

countvectorizer.vocabulary_
featurenames = countvectorizer.get_feature_names()

freqentlywords = zip(countvectorizer.get_feature_names(), vectortransformed.sum(axis=0).tolist()[0])
print(sorted(freqentlywords, key=lambda x: -x[1]))

#training the model
ldamodel = LatentDirichletAllocation(n_components=15, random_state=123, learning_method='batch')
topicmodel = ldamodel.fit(vectortransformed)

pipe = Pipeline([('vect', countvectorizer),('model', topicmodel)])

#saving the trained model
filename = 'model_vectorizer.pk'
pickle.dump(pipe, open(filename, 'wb'))






