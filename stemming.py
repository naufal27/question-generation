import nltk
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import json
import pandas as pd
import time
from datetime import timedelta

ft = open('stopword-ngram.json')
ft2 = json.load(ft)
df = pd.DataFrame(ft2)


def stemming(text):
    hasil = []
    for word in text:
        stem = StemmerFactory().create_stemmer().stem(word)
        hasil.append(stem)
    # stemmer = factory.create_stemmer()
    # hasil = stemmer.stem(text)
    return hasil


def tokenize(text):
    return nltk.tokenize.word_tokenize(text)


start_time = time.time()
df = df[0].apply(tokenize)
df = df.apply(stemming)
finish_time = time.time()
print('Finish dalam waktu : {}'.format(
    timedelta(seconds=finish_time-start_time)))

y = df.to_json(r'stemming-ngram.json',
               orient='records', indent=4)
print(df)
