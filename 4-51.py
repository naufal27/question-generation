import gensim
import json
import pandas as pd
import nltk

id_w2v = gensim.models.Word2Vec.load('wiki_w2v.model')
ft = open('comments_processed_test.json')
ft2 = json.load(ft)
ft3 = pd.DataFrame(ft2)


def tokenize(text):
    return nltk.tokenize.word_tokenize(text)


ft3 = ft3['text'].apply(tokenize)

non_formal_word = []
for comment in ft3:
    for sub_comment in comment:
        if sub_comment not in id_w2v.wv:
            non_formal_word.extend([sub_comment])
non_formal_word = set(non_formal_word)
non_formal_word = list(non_formal_word)
# with open('informal_word.txt', 'w', encoding='utf-8') as f:
#     json.dump(non_formal_word, f, ensure_ascii=False, indent=4)
# print(non_formal_word)

corpus = pd.read_csv('unformal word - Sheet1.csv')
letter = corpus[['kata normal', 'normal.1']]
letter.columns = ['unformal', 'normal']
pemisah = corpus[['pemisah', 'normal.3']]
pemisah.columns = ['unformal', 'normal']
singkatan = corpus[['singkatan', 'normal.4']]
singkatan.columns = ['unformal', 'normal']
hasil = pd.concat([letter, pemisah, singkatan], ignore_index=True)
hasil.dropna(inplace=True)
print(hasil.loc[hasil['unformal'] == 'smakin'])

# js = {
#     "aku": "saya",
#     "kamu": "kau"
# }
# jsl = json.load(js)
# ts = pd.read_json(js)
# print(ts)
