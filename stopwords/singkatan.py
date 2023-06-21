import pandas as pd
import nltk
abbrevation = [
    'tp',
    'smt',
    'lg',
    'ttp',
    'tgl',
    'udh',
    'yg',
    'ny',

]


def tokenize(text):
    # tokenized = text.split()
    tokenized = nltk.tokenize.word_tokenize(text)
    return tokenized


df = pd.read_csv('unformal word - singkatan.csv', names=['abbrevation'])
list = df.values.tolist()
flatten = nltk.flatten(list)
abbrevation_stopword = flatten
# print(abbrevation_stopword)
