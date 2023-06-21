# from slang_word import flatten
import re
from functools import reduce
import time
from datetime import timedelta
import pandas as pd
import json

corpus = pd.read_csv('unformal word - normalisasi.csv', na_values="")
# print(corpus.info())
slang = corpus[['gaul', 'normal']]
slang.columns = ['unformal', 'normal']
slang.dropna(inplace=True)
letter = corpus[['kata normal', 'normal.1']]
letter.columns = ['unformal', 'normal']
letter.dropna(inplace=True)
an_lang = corpus[['bahasa lain', 'normal.2']]
an_lang.columns = ['unformal', 'normal']
an_lang.dropna(inplace=True)
pemisah = corpus[['pemisah', 'normal.3']]
pemisah.columns = ['unformal', 'normal']
pemisah.dropna(inplace=True)
singkatan = corpus[['singkatan', 'normal.4']]
singkatan.columns = ['unformal', 'normal']
singkatan.dropna(inplace=True)
hasil = pd.concat([slang, letter, an_lang, pemisah,
                  singkatan], ignore_index=True)

# print(hasil)

ft = open('../comments_processed_test.json')
ft2 = json.load(ft)
ft3 = pd.DataFrame(ft2)

df = pd.DataFrame({
    'replace': ['word1', 'word2', 'word3', 'span ptkin', 'um ptkin', 'span', 'um'],
    'replace_with': ['new_word1', 'new_word2', 'new_word3', 'spanptkin', 'umptkin', 'spanptkin', 'umptkin']
})
df_text = pd.DataFrame({
    'text': ['This is word1 and word2 and word3.', 'aku word1tambah kamu', 'kamu kurangword3', 'mereka diaword2saya', 'aku span', 'kamu um', 'kita ptkin', 'mereka span ptkin', 'dia um ptkin', 'saya spanptkin', 'kau umptkin']
})

# example string to replace words in
string_to_replace = 'This is word1 and word2 and word3.'

# loop through each row in the DataFrame and replace words in the string
for i, row in df.iterrows():
    string_to_replace = string_to_replace.replace(
        row['replace'], row['replace_with'])


def nrmlz(text):
    nrlmzd = text
    for i, row in hasil.iterrows():
        nrlmzd = nrlmzd.replace(row['unformal'], row['normal'])
    return nrlmzd


def nrmlz2(text):
    replacements = {row['replace']: row['replace_with']
                    for _, row in df.iterrows()}
    return reduce(lambda acc, cur: acc.replace(*cur), replacements.items(), text)


# print the resulting string
# print(string_to_replace)
# print("Processing data...")
# start_time = time.time()
# ft3['text'] = ft3['text'].apply(nrmlz2)
# finish_time = time.time()
# print('Elapsed time: {}'.format(timedelta(seconds=finish_time-start_time)))
# json_tl = ft3['text']
# y = json_tl.to_json(r'tes_normalized.json',
#                     orient='records', indent=4)


def nrmlz3(text):
    # create dictionary from the DataFrame
    replace_dict = dict(zip(hasil['unformal'], hasil['normal']))

    # create regular expression pattern
    pattern = r'\b(' + '|'.join(re.escape(word)
                                for word in replace_dict.keys()) + r')\b'

    # replace words in the text using the regular expression pattern and the dictionary
    nrlmzd = re.sub(pattern, lambda x: replace_dict[x.group()], text)

    return nrlmzd


# df_text['text'] = df_text['text'].apply(nrmlz3)
ft3['text'] = ft3['text'].apply(nrmlz3)
json_tl = ft3['text']
y = json_tl.to_json(r'tes_normalized.json',
                    orient='records', indent=4)
print(ft3)

# print(flatten)
