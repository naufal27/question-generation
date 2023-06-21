import csv
import nltk
import pandas as pd

english = [
    'the',
    'congrats',
    'congratulations',
    'abah',
    'btw',
    'thank',
    'you',
    'of',
    'see',
    'first',
    'day',
]
sunda = [
    'can',
    'anggeus',
    'baheula',
    'mabal',
    'tinggaleun',
    'deui',
    'omaattt',
    'omat',
    'pinuh',
    'uhuy',
    'tamas',
    'ceng',
    'meni',
    'uyy',
    'ka',
    'ngiluan',
    'hiji',
    'nundutan',
    'th',
    'mah',
    'hatur',
    'nuhun',
    'mangga',
]


def tokenize(text):
    # tokenized = text.split()
    tokenized = nltk.tokenize.word_tokenize(text)
    return tokenized


# csv_file = "unformal word - bahasa lain.csv"

# with open(csv_file, 'r') as f:
#     csv_reader = csv.reader(f)
#     header = next(csv_reader)
#     data = [row for row in csv_reader]

df = pd.read_csv('unformal word - bahasa lain.csv', names=['an_lang'])
list = df.values.tolist()
flatten = nltk.flatten(list)
an_lang_stopword = flatten
# print(an_lang_stopword)
