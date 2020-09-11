import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import text 
from sklearn.decomposition import LatentDirichletAllocation
import pickle
from sklearn.pipeline import Pipeline

loaded_model = pickle.load(open("./ml_models/model_vectorizer.pk", 'rb'))
countvect = loaded_model['vect']
ldamodel = loaded_model['model']
featurenames = countvect.get_feature_names()
ldamodel
top = 12
for x, y in enumerate(ldamodel.components_):    
    print(x +1)
    print(" ".join([featurenames[l] for l in y.argsort()[:-top-1:-1]]))