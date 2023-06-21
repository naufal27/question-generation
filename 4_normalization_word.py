import gensim
from datetime import timedelta
import pandas as pd
import time
import json
import nltk

slang_corpus = pd.read_csv('colloquial-indonesian-lexicon.csv')
slang_corpus = slang_corpus[slang_corpus.columns[0:2]]

# corpus = pd.read_csv('unformal word - Sheet1 (1).csv')
# letter = corpus[['kata normal', 'normal.1']]
# letter.columns = ['unformal', 'normal']
# letter.dropna(inplace=True)
# pemisah = corpus[['pemisah', 'normal.3']]
# pemisah.columns = ['unformal', 'normal']
# pemisah.dropna(inplace=True)
# singkatan = corpus[['singkatan', 'normal.4']]
# singkatan.columns = ['unformal', 'normal']
# singkatan.dropna(inplace=True)
# hasil = pd.concat([letter, pemisah, singkatan], ignore_index=True)

ft = open('comments_processed_test.json')
ft2 = json.load(ft)
ft3 = pd.DataFrame(ft2)


def tokenize(text):
    return nltk.tokenize.word_tokenize(text)


ft3 = ft3['text'].apply(tokenize)
# print(ft3)

########################
print("Processing data...")
start_time = time.time()
corr_comments = []
slang_words = []
reco_words = []
corr_word = 0
tot_word = 0
id_w2v = gensim.models.Word2Vec.load('wiki_w2v.model')
for comment in ft3:
    corr_comment = []
    slang_word = []
    for sub_comment in comment:
        if sub_comment in id_w2v.wv:
            sim_slang = slang_corpus[slang_corpus['slang'] == sub_comment]
            if len(sim_slang) != 0:
                mode_word = sim_slang.formal.mode()[0]
                corr_word = corr_word + 1
                corr_comment.append(mode_word)
            else:
                corr_word = corr_word + 1
                corr_comment.append(sub_comment)
        else:
            comment_found = False
            sim_slang = slang_corpus[slang_corpus['slang'] == sub_comment]
            if len(sim_slang) != 0:
                mode_word = sim_slang.formal.mode()[0]
                corr_word = corr_word + 1
                corr_comment.append(mode_word)
                comment_found = True
            # else:
            #     rat_words = []
            #     for slang in hasil['unformal']:
            #         rat_word = nltk.edit_distance(sub_comment, slang)
            #         rat_words.append(rat_word)
            #     min_rat = rat_words.index(min(rat_words))
            #     value = str(hasil.normal.loc[min_rat])
            #     corr_words = corr_word + 1
            #     corr_comment.append(value)
            #     slang_words.append(sub_comment + " = " + value)
            #     comment_found = True
            if comment_found == False:
                corr_comment.append(sub_comment)
                slang_words.append(sub_comment + " = " + "Not Found")
        tot_word = tot_word + 1
    corr_comments.append(corr_comment)
    print("Total kata yang sudah diproses : " + str(tot_word))
print("Total kata yang diperbaiki : " + str(corr_word) +
      " dari total semua kata : " + str(tot_word))
finish_time = time.time()
print('Elapsed time: {}'.format(timedelta(seconds=finish_time-start_time)))
# print(corr_comments)
########################
with open('comments_normalized.json', 'w', encoding='utf-8') as f:
    json.dump(corr_comments, f, ensure_ascii=False, indent=4)
# list_json = json.dumps(corr_comments)

# print(ft3)

# Spell Checker
# sym_spell = SymSpell()
# path_corpus = open("wiki.txt", encoding="utf8")
# sym_spell.create_dictionary(path_corpus)

# def spell_checker(text):
#     for w in text:
#         suggestions = sym_spell.lookup(w, Verbosity.CLOSEST, max_edit_distance=2, include_unknown=True)
#         print(f"'{w}' -> '{[s.term for s in suggestions][0]}'")
# df['text'] = df["text"].apply(spell_checker)
# print(df['text'].head(5))

# test_words = ['kcing', 'memkan', 'mrdeka', 'mnyedihkan', 'gimna',
#               'terdpt', 'mrmpersulit', 'mhon', 'banos', 'begimana']
# import time
# start = time.time()
# for w in test_words:
#     suggestions = sym_spell.lookup(w, Verbosity.CLOSEST, max_edit_distance=2, include_unknown=True)
#     print(f"'{w}' -> '{[s.term for s in suggestions][0]}'")
# end = time.time()
# print(f'{end-start} detik')
