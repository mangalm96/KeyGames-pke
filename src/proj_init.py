#!/usr/bin/env python
# coding: utf-8

# In[ ]:


## load packages

import spacy
nlp=spacy.load('en_core_web_lg')
import pickle
import numpy as np
import nltk
import re
import glob
import os
from gensim import models, corpora
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
import string
stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()
from fuzzywuzzy import fuzz
import logging
from itertools import compress, count, islice
from functools import partial
from operator import eq
import pke
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer(language='english')


# In[ ]:


## setup stop word list

with open('fwlist-277.txt', 'r') as myfile:
    functional=myfile.read().replace('\n', ' ')
functional=functional.split()
with open('SmartStoplist.txt', 'r') as smartfile:
    smart_stop=smartfile.read().replace('\n', ' ')
smart_stop=smart_stop.split()
stop = set(stopwords.words('english'))
stop.remove('and')
stop.remove('or')

stop_phrase=["user","mechanisms","mechanism","observations","observation","applications","application","observed","effortless","user","benefecial","enhanced","enhance","new","deployed","significant","various","repeated","enthusiastic","approach","major","admissible","regular","innovative","developed","previous","original","existing","improved","efficient",
             "proposed","sophisticated","robust","modern","advanced","original","paper","required","existing "
            "potential","widely","usual","resulting","successful","earlier","excellent","obtained","inherently"
            ,"underlying","important","constructive","effective","revolutionary","heavily","repeated"]


# In[ ]:


# load fasttext model
from gensim.models import FastText
model1 = FastText.load_fasttext_format('wiki-news-300d-1M-subword.bin')


# In[ ]:


## import title file

# with open ('semeval_TITLE_XML', 'rb') as fp:
#     title_file = pickle.load(fp)
    
# with open ('duc_title2', 'rb') as fp:
#     title_file = pickle.load(fp)

with open ('inspec_title', 'rb') as fp:
    title_file = pickle.load(fp)

