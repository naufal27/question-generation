# from sklearn.decomposition import NMF
# from sklearn.decomposition import LatentDirichletAllocation
# from sklearn.pipeline import make_pipeline
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.feature_extraction.text import CountVectorizer
# import json
# import pandas as pd

# ft = open('comments_stopworded.json')
# ft2 = json.load(ft)
# df = pd.DataFrame(ft2)
# # print(df[0])

# c_vec1 = CountVectorizer(ngram_range=(2, 2))
# c_vec2 = CountVectorizer(ngram_range=(3, 3))

# ngrams1 = c_vec1.fit_transform(df[0])
# ngrams2 = c_vec2.fit_transform(df[0])

# count_values1 = ngrams1.toarray().sum(axis=0)
# count_values2 = ngrams2.toarray().sum(axis=0)

# vocab1 = c_vec1.vocabulary_
# vocab2 = c_vec2.vocabulary_

# df_ngram1 = pd.DataFrame(sorted([(count_values1[i], k) for k, i in vocab1.items(
# )], reverse=True)).rename(columns={0: 'frekuensi', 1: 'bigram'})
# print(df_ngram1.info())
# df_ngram2 = pd.DataFrame(sorted([(count_values2[i], k) for k, i in vocab2.items(
# )], reverse=True)).rename(columns={0: 'frekuensi', 1: 'trigram'})
# print(df_ngram2.head(50))

# #####################
# # LDA MODELS

# tfidf_vectorizer = TfidfVectorizer(ngram_range=(3, 3))
# lda = LatentDirichletAllocation(n_components=3)
# pipe = make_pipeline(tfidf_vectorizer, lda)
# pipe.fit(df[0])


# def print_top_words(model, feature_names, n_top_words):
#     for topic_idx, topic in enumerate(model.components_):
#         message = "LDA #%d: " % topic_idx
#         message += ", ".join([feature_names[i]
#                               for i in topic.argsort()[:-n_top_words - 1:-1]])
#         print(message)
#     print()


# print_top_words(lda, tfidf_vectorizer.get_feature_names_out(), n_top_words=3)
# ############################

# ############################
# # NMF MODELS

# tfidf_vectorizer2 = TfidfVectorizer(ngram_range=(3, 3))
# nmf = NMF(n_components=3)
# pipe2 = make_pipeline(tfidf_vectorizer2, nmf)
# pipe2.fit(df[0])

# print_top_words(nmf, tfidf_vectorizer2.get_feature_names_out(), n_top_words=3)
# ############################

import pandas as pd
import re
import nltk
import json
text = ['halo selamatnya', 'dimananya kamu',
        'disini aku nya', 'ada span ptkin ada', 'ada um ptkin', 'ada spanptkin', 'ada umptkin']
df = pd.DataFrame({'test': text})
tesin = ['span ptkin', 'spanptkin', 'um ptkin', 'umptkin']
r = df[df['test'].str.contains('|'.join(tesin))]


def singatan(text):
    tergabung = text.replace('ptkin', '')
    tergabung = tergabung.replace('span', 'spanptkin')
    tergabung = tergabung.replace('um', 'umptkin')
    return tergabung


r['test'] = r['test'].apply(singatan)
# print(r)

k = ''
t2 = 'halo dimananya banyaknya disini sebelahnya kemendikbud diam span ptkin'
t3 = nltk.tokenize.word_tokenize(t2)
t4 = t2.split()
for i in range(len(t3)):
    if t3[i].endswith('nya'):
        j = t3[i][:-3]
        j = ' '.join([j, 'nya'])
        t3[i] = j
        if t3[i].startswith('di'):
            k = t3[i][2:]
            k = ' '.join(['di', k])
            t3[i] = k
    elif t3[i].startswith('di'):
        if (t3[i].startswith('di')) & (not t3[i].startswith('dia')):
            j = t3[i][2:]
            j = ' '.join(['di', j])
            t3[i] = j
    else:
        print()
# print(t3)
# print(t4)


# jf = json.load(open(
#     'F:\\Coba Project TA\\instaloader\\uinsgd.official_comments\\2023-02-26_13-32-08_UTC_comments.json'))
# data = []
# data.append('a')
# print(data)
# for k, v in jf.items():
#     print(k, ':', v)
# data.extend()


ls = ['ke 10', '20 ke', '423232 ke 30 kdadasa dadsa 111231', 'empat lima2',
      ' tes2 2aku', 's2 jadi2 2tanda', 'tanda2 kiamat', 'aku s1 kamus1']
df = pd.DataFrame(ls)
li = ['satu', 'dua', 'tiga', 'empat']
li = set(li)


def test(text):
    return [word for word in text if word not in li]


def tokenize(text):
    # tokenized = text.split()
    tokenized = nltk.tokenize.word_tokenize(text)
    return tokenized


def preprocessing(text):
    # processed = re.sub(r"\d+", "", text)   # remove number
    # processed = re.sub(r"\w+[^s][2]\b", "", text)   # remove number
    sementara = "\\w+[$s][2]\\b"
    s1 = "s1"
    s2 = "s2"
    se = fr"{s1}(?!{s2})"
    # processed = re.sub(r"{}".format(sementara), "",
    #                    processed)   # remove number
    pattern = r"\b(\w+)(2)\b(?<!s2)"
    processed = re.sub(pattern, lambda match: match.group(1)*2,
                       text)   # remove number
    processed = re.sub(r"\b\d+\b", "", processed)
    return processed


# df[0] = df[0].apply(tokenize)
df[0] = df[0].apply(preprocessing)
print(df)
