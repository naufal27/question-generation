import numpy as np
from nltk.tokenize.treebank import TreebankWordDetokenizer
import nltk
import json
import pandas as pd

ft = open('comments_normalized.json')
ft2 = json.load(ft)
df = pd.DataFrame({'text': ft2})

slang = [
    'mantap',
    'owalah',
    'lu',
    'enggak',
    'gak',
    'ga',
    'wow',
    'banget',
    'gini',
    'amat',
    'kok',
    'makin',
    'wkwk',
    'kangen',
    'dm',
    'anjrit',
    'eh',
    'yaa',
    'nih',
    'tuh',
    'deh',
    'udah',
    'gaada',
    'wih',
    'hihi',
    'wihh',
    'wihhhh',
    'ajeh',
    'gaskeun',
    'gua',
    'nyari',
    'ngapain',
    'pengen',
    'dah',
    'nyimaq',
    'kek',
    'bgt',
    'yeay',
    'mon',
    'maap',
    'anggurin',
    'aduhh',
    'nich',
    'bagiin',
    'bg',
    'kate',
    'yee',
    'tipsen',
    'huhuhu',
    'nunggu',
    'ahh',
    'loh',
    'titip',
    'netijen',
    'klo',
    'waahhh',
    'kerennn',
    'lohh',
    'ngajuin',
    'wuuuu',
    'emg',



    'almet',
    'katnya',
    'kumpulin',
    'dikumpulin',
    'bagiaan',
    'fto',
    'dftr',
    'gmna',
    'yng',
    'karfu',
    'brlaku',
    'dapetin',
    'dmn',
    'gmn',
    'pakultas',
    'gimna',
    'semangaat',
    'manaa',
    'kno',
    'masi',
    'msh',
    'matkul',
    'nerima',
    'knapa',
    'apaa',


]

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

an_lang = [
    # sunda
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
    # english
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

word_segmentation = [

]

word_normalization = {
    "": "",
}

slang = set(slang)
abbrevation = set(abbrevation)
an_lang = set(an_lang)


def remove_slang(text):
    return [word for word in text if word not in slang]


def remove_abbrevation(text):
    return [word for word in text if word not in abbrevation]


def remove_an_lang(text):
    return [word for word in text if word not in an_lang]


def de_tokenize(text):
    return TreebankWordDetokenizer().detokenize(text)


def tokenize(text):
    # tokenized = text.split()
    tokenized = nltk.tokenize.word_tokenize(text)
    return tokenized


# df['text'] = df['text'].apply(tokenize)
df['text'] = df['text'].apply(remove_slang)
df['text'] = df['text'].apply(remove_abbrevation)
df['text'] = df['text'].apply(remove_an_lang)
df['text'] = df['text'].apply(de_tokenize)

df['text'].replace('', np.nan, inplace=True)
df.dropna(inplace=True)
df.reset_index(drop=True, inplace=True)
json_tl = df['text']
y = json_tl.to_json(r'comments_slang-abb.json', orient='records', indent=4)
print(df)
