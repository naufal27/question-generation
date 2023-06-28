import nltk
import json
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize.treebank import TreebankWordDetokenizer

ft = open('stemming-ngram.json')
ft2 = json.load(ft)
# df = pd.DataFrame(ft2)
df = pd.DataFrame({0: ft2})
# print(df)


def de_tokenize(text):
    return TreebankWordDetokenizer().detokenize(text)


df[0] = df[0].apply(de_tokenize)
# print(df)

c_vec1 = CountVectorizer(ngram_range=(2, 2))

ngrams1 = c_vec1.fit_transform(df[0])

count_values1 = ngrams1.toarray().sum(axis=0)

vocab1 = c_vec1.vocabulary_

df_ngram1 = pd.DataFrame(sorted([(count_values1[i], k) for k, i in vocab1.items(
)], reverse=True)).rename(columns={0: 'frekuensi', 1: 'bigram'})
# ts = df_ngram1[df_ngram1['frekuensi'] >= 10]
ts = df_ngram1.head(15)
print(ts)

cf = open('stemming.json')
cf2 = json.load(cf)
cf3 = pd.DataFrame({0: cf2})
# print(cf3)
cf3[0] = cf3[0].apply(de_tokenize)

question_filtered = {}
ngram_result = ts['bigram'].values.tolist()
for item in ngram_result:
    qf2 = cf3[cf3[0].str.contains(item)]
    baru = qf2[0].values.tolist()
    question_filtered[item] = baru


def tokenize(text):
    tokenized = nltk.tokenize.word_tokenize(text)
    return tokenized


def stopword_rm(text):
    return [word for word in text if word in ngram_result]


with open('ngram.json', 'w', encoding='utf-8') as f:
    json.dump(question_filtered, f, ensure_ascii=False, indent=4)
