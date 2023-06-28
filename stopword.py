import numpy as np
import json
import pandas as pd
from nltk.corpus import stopwords
import re
from nltk.tokenize.treebank import TreebankWordDetokenizer
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import nltk

ft = open('cleansing.json')
ft2 = json.load(ft)
df = pd.DataFrame(ft2, columns=['text'])

stopword_nltk = stopwords.words('indonesian')
stopword_sastrawi = StopWordRemoverFactory().get_stop_words()
tambahan = [
    'uin', 'bandung', 'sgd', 'innalillahi', 'wa', 'inna', 'sunan', 'gunung', 'djati', 'innailaihi', 'kalo',
    'ilaihi', 'min', 'masya', 'allah', 'rojiun', 'ga', 'hatur', 'nuhun', 'nya', 'kasih', 'husnul', 'khotimah',
    'wainna', 'syaa', 'selamat', 'keren', 'banget', 'jalan', 'na', 'waafihi', 'wafuanhu', 'iya', 'nih',
    'dm', 'assalamualaikum', 'kak', 'warhamhu', 'century', 'girl', 'proud', 'of'
]
all_stopword = stopword_nltk + stopword_sastrawi + tambahan
ls_sw = set(all_stopword)
kecuali = {'apa', 'siapa', 'kapan', 'mengapa',
           'bagaimana', 'dimana', 'berapa', 'kenapa'}
# ls_sw = ls_sw - kecuali


def just_number(text):
    # return re.sub(r'\b\d+\b', '', text)  # remove just numbers
    kalimat_tanpa_nomor = ''.join(
        karakter for karakter in text if not karakter.isdigit())
    return kalimat_tanpa_nomor


def single_char(text):
    return re.sub(r"\b[a-zA-Z]\b", "", text)  # remove single char


def space(text):
    processed = text.strip()   # remove whitespace start and end
    processed = " ".join(re.split("\s+", processed, flags=re.UNICODE))
    return processed


def stopword_rm(text):
    return [word for word in text if word not in ls_sw]


def de_tokenize(text):
    return TreebankWordDetokenizer().detokenize(text)


def tokenize(text):
    # tokenized = text.split()
    tokenized = nltk.tokenize.word_tokenize(text)
    return tokenized


def rename(text):
    hasil = re.sub(r'span ptkin\b', 'spanptkin', text)
    hasil = re.sub(r'span\b', 'spanptkin', hasil)
    hasil = re.sub(r'um ptkin\b', 'umptkin', hasil)
    hasil = re.sub(r'\bum\b', 'umptkin', hasil)
    return hasil


df['text'] = df['text'].apply(tokenize)
df['text'] = df['text'].apply(stopword_rm)
df['text'] = df['text'].apply(de_tokenize)
df['text'] = df['text'].apply(just_number)
df['text'] = df['text'].apply(single_char)
df['text'] = df['text'].apply(rename)
# df['text'] = df['text'].apply(rename2)
df['text'] = df['text'].apply(space)


df['text'].replace('', np.nan, inplace=True)
# df.dropna(subset=['text'], inplace=True)
df.dropna(inplace=True)
df.reset_index(drop=True, inplace=True)
json_tl = df['text']
y = json_tl.to_json(r'stopword-ngram.json',
                    orient='records', indent=4)
print(df)
