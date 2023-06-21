import nltk
import json
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer


ft = open('comments_stopworded_test.json')
ft2 = json.load(ft)
df = pd.DataFrame(ft2)
# print(df[0])

c_vec1 = CountVectorizer(ngram_range=(2, 2))
c_vec2 = CountVectorizer(ngram_range=(3, 3))
c_vec3 = CountVectorizer(ngram_range=(1, 1))

ngrams1 = c_vec1.fit_transform(df[0])
ngrams2 = c_vec2.fit_transform(df[0])
ngrams3 = c_vec3.fit_transform(df[0])

count_values1 = ngrams1.toarray().sum(axis=0)
count_values2 = ngrams2.toarray().sum(axis=0)
count_values3 = ngrams3.toarray().sum(axis=0)

vocab1 = c_vec1.vocabulary_
vocab2 = c_vec2.vocabulary_
vocab3 = c_vec3.vocabulary_

df_ngram1 = pd.DataFrame(sorted([(count_values1[i], k) for k, i in vocab1.items(
)], reverse=True)).rename(columns={0: 'frekuensi', 1: 'bigram'})
# ts = df_ngram1[df_ngram1['frekuensi'] >= 10]
ts = df_ngram1.head(15)
print(ts)
df_ngram2 = pd.DataFrame(sorted([(count_values2[i], k) for k, i in vocab2.items(
)], reverse=True)).rename(columns={0: 'frekuensi', 1: 'trigram'})
# ts2 = df_ngram2[df_ngram2['frekuensi'] >= 5]
ts2 = df_ngram2.head(15)
# print(ts2)
df_ngram3 = pd.DataFrame(sorted([(count_values3[i], k) for k, i in vocab3.items(
)], reverse=True)).rename(columns={0: 'frekuensi', 1: 'unigram'})
# ts3 = df_ngram3[(df_ngram3['frekuensi'] < 12) &
#                 (df_ngram3['frekuensi'] >= 11)]
ts3 = df_ngram3.head(20)
# print(ts3)

co_file = open('comments_processed_test.json')
co_file2 = json.load(co_file)
co_file3 = pd.DataFrame(co_file2)
cf = open('comments_stopworded_test.json')
cf2 = json.load(cf)
cf3 = pd.DataFrame(cf2)

question_filtered = {}
ngram_result = ts['bigram'].values.tolist()
# ngram_result.append()
# for item in ngram_result:
#     qf = co_file3[co_file3['text'].str.contains(item)]
#     qf2 = cf3[cf3[0].str.contains(item)]
#     baru = qf['text'].values.tolist()
#     baru.extend(qf2[0].values.tolist())
#     question_filtered[item] = baru
# dict.fromkeys(item, co_file3['text'])
# print(len(question_filtered))


def tokenize(text):
    # tokenized = text.split()
    tokenized = nltk.tokenize.word_tokenize(text)
    return tokenized


def stopword_rm(text):
    return [word for word in text if word in ngram_result]


qf = cf3[0].values.tolist()
filtered_sentences = [sentence for sentence in qf if any(
    word in sentence for word in ngram_result)]
# print(qf)
# qf['text'] = co_file3['text'].apply(tokenize)
# qf['text'] = co_file3['text'].apply(stopword_rm)
# for item in ngram_result:
#     question_filtered[item] = qf['text'].values.tolist()
with open('comments_ngram.json', 'w', encoding='utf-8') as f:
    json.dump(filtered_sentences, f, ensure_ascii=False, indent=4)
