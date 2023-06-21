import pandas as pd
import nltk


def tokenize(text):
    # tokenized = text.split()
    tokenized = nltk.tokenize.word_tokenize(text)
    return tokenized


df = pd.read_csv('unformal word - pemisah.csv', names=['separator'])
list = df.values.tolist()
flatten = nltk.flatten(list)
separator_stopword = flatten
# print(separator_stopword)
