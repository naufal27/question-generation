import re
from stopwords.an_lang import an_lang_stopword
from stopwords.separator import separator_stopword
from stopwords.singkatan import abbrevation_stopword
from stopwords.slang_word import slang_stopword
from stopwords.tambahan import add
import pandas as pd
import nltk
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.corpus import stopwords
import json
import numpy as np
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from datetime import timedelta
import time
# nltk.download()

# ft = open('stopwords/tes_normalized.json')
ft = open('comments_normalized.json')
ft2 = json.load(ft)
df = pd.DataFrame({'text': ft2})
# df = pd.DataFrame(ft2)
# test_list2 = TreebankWordDetokenizer().detokenize([test_list])


ls_sw = stopwords.words('indonesian')
ls_sw.extend([
    # uin
    'uin',
    'sunan',
    'gunung',
    'djati',
    'sgd',
    # panggilan
    'abang',
    'kakak',
    'kaka',
    'kak',
    'teh',
    'kang',
    'min',
    'miin',
    'minn',

    'hai',
    'halo',
    'pak',
    'saya',
    'aku',
    'kita',
    'beliau',
    'akang',
    'teteh',
    #
    # 'nunggu',
    # 'selamat',
    # 'biar',
    # 'ambil',
    # 'semoga',
    # 'salah',
    # 'depan',
    # 'mohon',
    # 'jawab',
    # 'tiba',
    # 'harus',
    'keren',
    # 'terima',
    'kasih',
    '20th',
    # 'makasih',
    'mudahan',
    'maaf',
    'of',
    'cepat',
    # 'bisa',
    # 'tidak',
    # 'sudah',
    # 'biasa',
    # 'lewat',
    # 'selalu',
    # 'belum',
    # 'disini',
    # 'mau',
    # 'buat',
    # 'sama',
    # 'masih',
    # 'dulu',
    # 'nanti',
    # kata sambung
    'an',
    'kan',
    'atau',
    'tapi',
    'jadi',
    'dari',
    'itu',
    'lagi',
    'tau',
    'dan',
    'aja',
    'ada',
    'ini',
    'ke',
    'ya',
    'dong',
    'nya',
    'yuk',
    'sih',
    'iya',
    'jangan',
    'juga',
    'yang',
    'di',
    'untuk',
    # katatanya
    'berapa',
    'kapan',
    'siapa',
    'apa',
    'nanya',
    'tanya',
    'kah',
    'apakah',
    'bertanya',
    'gimana',
    'kalo',
    'kalau',
    'bolehkah',
    'mana',
    # agama
    'ya allah',
    'assalamualaikum',
    'ma',
    'maa',
    'allaah',
    'syaa',
    'alhamdulillah',
    'alhamdulillaah',
    'bismillah',
    'masyaallah',
    'masyallah',
    'masya',
    'allah',
    'amin',
    'aamiin',
    'inna',
    'lillahi',
    'wa',
    'ilaihi',
    'rojiun',
    'rajiun',
    'wainna',
    'innalillahi',
    'innalilahi',
    'innailaihi',
    'wainnailaihi',
    'husnul',
    'khotimah',
    'warhamhu',
    'waafihi',
    'wafuanhu',
    'allahummaghfirlahu',
    'baarokalloh',
    'fiikum',
    'allohumma',
    'sollialla',
    'sayyidina',

])
# ls_sw.extend([


# ])

ls_sw.extend(an_lang_stopword)
ls_sw.extend(separator_stopword)
ls_sw.extend(abbrevation_stopword)
ls_sw.extend(slang_stopword)
ls_sw.extend(add)
ls_sw = set(ls_sw)


def just_number(text):
    return re.sub(r"\b\d+\b", "", text)  # remove just numbers


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


# print('start')
# start_time = time.time()
# df['text'] = df['text'].apply(de_tokenize)
# print('detokenized')
# df['text'] = df['text'].apply(stemming)
# print('stemmed')
# df['text'] = df['text'].apply(tokenize)
df['text'] = df['text'].apply(stopword_rm)
df['text'] = df['text'].apply(de_tokenize)
df['text'] = df['text'].apply(just_number)
df['text'] = df['text'].apply(single_char)
df['text'] = df['text'].apply(space)
# finish_time = time.time()
# print(df)

df['text'].replace('', np.nan, inplace=True)
# df.dropna(subset=['text'], inplace=True)
df.dropna(inplace=True)
df.reset_index(drop=True, inplace=True)
json_tl = df['text']
y = json_tl.to_json(r'comments_stopworded_test.json',
                    orient='records', indent=4)
print(df)
# print('Elapsed time: {}'.format(timedelta(seconds=finish_time-start_time)))
