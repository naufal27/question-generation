import pandas as pd
import nltk


def tokenize(text):
    # tokenized = text.split()
    tokenized = nltk.tokenize.word_tokenize(text)
    return tokenized


df = pd.read_csv('unformal word - tambahan.csv', names=['add'])
list = df.values.tolist()
flatten = nltk.flatten(list)
add = flatten
