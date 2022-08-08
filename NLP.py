import io
import random
import string # to process standard python strings
import warnings
import numpy as np
import pymysql
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
nltk.download('popular', quiet=True) # for downloading packages



with open('text.txt','r', encoding='utf8', errors ='ignore') as fin:
    raw = fin.read().lower()

#TOkenisation
sent_tokens = nltk.sent_tokenize(raw)# converts to list of sentences
word_tokens = nltk.word_tokenize(raw)# converts to list of words

# Preprocessing
lemmer = WordNetLemmatizer()

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

def response(user_response):
    robo_response=''
    sent_tokens.append(user_response)
    final_stopwords_list = stopwords.words('english') + stopwords.words('french')
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words=final_stopwords_list )
    tfidf =TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    sent_tokens.remove(user_response)
    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I don't understand you , can you specify"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response

