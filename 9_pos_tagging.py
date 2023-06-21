import flair.datasets
from flair.embeddings import TokenEmbeddings, WordEmbeddings, StackedEmbeddings, BertEmbeddings
from typing import List
from flair.models import SequenceTagger
from flair.trainers import ModelTrainer
from flair.data import Sentence

# corpus = flair.datasets.UD_INDONESIAN()

# tag_type = 'upos'
# tag_dictionary = corpus.make_tag_dictionary(tag_type=tag_type)

# embedding_types: List[TokenEmbeddings] = [
#     WordEmbeddings('id-crawl'),
#     WordEmbeddings('id'),
# ]
# embeddings: StackedEmbeddings = StackedEmbeddings(embeddings=embedding_types)

# tagger: SequenceTagger = SequenceTagger(
#     hidden_size=256, embeddings=embeddings, tag_dictionary=tag_dictionary, tag_type=tag_type, use_crf=True)

# trainer: ModelTrainer = ModelTrainer(tagger, corpus)
# trainer.train('resources/taggers/example-universal-pos',
#               learning_rate=0.1, mini_batch_size=32, max_epochs=10)

import json
import pandas as pd
f = open('comments_ngram_test.json')
f2 = json.load(f)

tag_pos = SequenceTagger.load(
    'resources/taggers/example-universal-pos/best-model.pt')
# sentence = Sentence(
#     'saya dan dia kemarin pergi ke pasar bersama untuk membeli jeruk. aku padamu')
# tag_pos.predict(sentence)
# # for s in sentence:
# #     print(s)
# print(sentence.to_tagged_string())
pos_tagged = []
for k, v in f2.items():
    for va in v:
        sentence = Sentence(va)
        tag_pos.predict(sentence)
        # print()
        pos_tagged.append(sentence.to_tagged_string())
# print(pos_tagged)
with open('comments_postag.json', 'w', encoding='utf-8') as f:
    json.dump(pos_tagged, f, ensure_ascii=False, indent=4)
