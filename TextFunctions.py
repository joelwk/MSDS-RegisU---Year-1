import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime


import nltk
from nltk.stem import WordNetLemmatizer
#nltk.download('wordnet')
from nltk.corpus import stopwords
stop = stopwords.words('english')

import warnings
##################################################################################################
def supportngcols(df, add_stopw):
    text = df.summary
    stop.extend(add_stopw)
    df['word_cnt'] = text.apply(lambda x: len(str(x).split(" ")))
    df['char_cnt'] = text.str.len()                     
    #Count words
    df['word_cnt'] = text.apply(lambda x: len(str(x).split(" ")))
    #Count number of characters
    df['char_cnt'] = text.str.len()
    #Count stopwords
    df['stopwords'] = text.apply(lambda x: len([x for x in x.split() if x in stop]))
    return df
##################################################################################################
def transformtext(df, add_stopw):
    text = df.summary
    #Lower case
    text = text.apply(lambda x: " ".join(x.lower() for x in x.split()))
    
    #Remove Web Addresses and User_ids
    text = text.str.replace('\S+@\S+','') #looking for the case of XXXX@XXXX
    text = text.str.replace('http\S+','') #looking for http or https web addresses
    text = text.str.replace('\S+.com','') #looking for email addresses that end in '.com'
    text = text.str.replace('\S+.edu','') #looking for email addresses that end in '.edu'

    #Remove punctuation
    text = text.str.replace('[^\w\s]','')

    #Remove digits
    text = text.str.replace('\d+','')
    
    #Remove stopwords
    stop.extend(add_stopw)
    text = text.apply(lambda x: " ".join(w for w in x.split() if w not in stop))
    
    #Word tokenization
    tokens = ' '.join(text).split()
    
    #Lemmatization
    wordnet_lemmatizer = WordNetLemmatizer()
    text = text.apply(lambda x: " ".join(wordnet_lemmatizer.lemmatize(w) for w in x.split()))
    df['summary_clean'] = text
    return df
##################################################################################################
def prep_WC(text):
    #Text Visualization - WordCloud
    freq = pd.Series(' '.join(text).split()).value_counts().to_dict()
    #Remove words not english
    text = text.apply(lambda x: ' '.join(x for x in x.split() if len(x) > 1))
    freq = pd.Series(' '.join(text).split()).value_counts().to_dict()
    freq_dist_WC = list(freq.items())[:20]
    return text, freq, freq_dist_WC
##################################################################################################
def transform_ngram(df):
    text = df.summary
    #Prep n-gram
    tokens = ' '.join(text).split()
    
    ngrams_2 = nltk.bigrams(tokens)
    freq_2grams = pd.Series(ngrams_2).value_counts().to_dict()
    ngram_2gramList = list(freq_2grams.items())[:20]
    
    ngrams_3 = nltk.trigrams(tokens)
    freq_3grams = pd.Series(ngrams_3).value_counts().to_dict()
    ngram_3gramList = list(freq_3grams.items())[:20]
    return ngram_2gramList, ngram_3gramList


